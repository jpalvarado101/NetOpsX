import React, { useEffect, useState } from 'react';
import Dashboard from './components/Dashboard';
import ManualOverride from './components/ManualOverride';
import { getTransactions } from './services/api';

const App: React.FC = () => {
  const [transactions, setTransactions] = useState<any[]>([]);

  useEffect(() => {
    // Fetch initial transactions
    getTransactions().then(data => setTransactions(data));

    // Establish WebSocket connection for real-time updates
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "new_transaction") {
        setTransactions(prev => [message.transaction, ...prev]);
      } else if (message.type === "override") {
        setTransactions(prev =>
          prev.map(tx => (tx.id === message.transaction.id ? message.transaction : tx))
        );
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>NetOpsX Dashboard</h1>
      <ManualOverride />
      <Dashboard transactions={transactions} />
    </div>
  );
};

export default App;
