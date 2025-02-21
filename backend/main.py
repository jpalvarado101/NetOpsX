import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import Transaction, Base
from database import engine, SessionLocal
from ai_routing import get_optimal_route
from simulation import simulate_transaction
from cloud_simulation import create_bucket, create_dynamodb_table, upload_sample_file

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeps the connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/transactions")
async def get_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    db.close()
    return transactions

@app.post("/transactions/override")
async def manual_override(request: Request):
    data = await request.json()
    transaction_id = data.get("id")
    new_route = data.get("new_route")
    db = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        transaction.route = new_route
        db.commit()
        db.refresh(transaction)
        await manager.broadcast({
            "type": "override",
            "transaction": {
                "id": transaction.id,
                "status": transaction.status,
                "route": transaction.route,
            }
        })
        db.close()
        return {"message": "Override updated", "transaction": transaction.id}
    db.close()
    return {"error": "Transaction not found"}

@app.post("/process/{transaction_id}")
async def trigger_lambda(transaction_id: str, background_tasks: BackgroundTasks):
    # Simulate AWS Lambda-like processing using a background task.
    background_tasks.add_task(process_transaction, transaction_id)
    return {"message": f"Transaction {transaction_id} is being processed in the background."}

def process_transaction(transaction_id: str):
    print(f"Simulated Lambda: Processing transaction {transaction_id}")

# Background task to simulate transactions every 5 seconds
async def background_simulator():
    while True:
        await asyncio.sleep(5)
        db = SessionLocal()
        # Simulate a new transaction event
        transaction_data = simulate_transaction()
        optimal_route = get_optimal_route(transaction_data)
        transaction = Transaction(
            status=transaction_data["status"],
            route=optimal_route
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        # Broadcast the new transaction to connected clients
        await manager.broadcast({
            "type": "new_transaction",
            "transaction": {
                "id": transaction.id,
                "status": transaction.status,
                "route": transaction.route,
            }
        })
        db.close()

@app.on_event("startup")
async def startup_event():
    # Start the transaction simulator
    asyncio.create_task(background_simulator())
    # Simulate cloud environment by creating bucket/table and uploading a file.
    create_bucket()
    create_dynamodb_table()
    upload_sample_file()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
