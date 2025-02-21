import boto3
from botocore.config import Config

# S3 client for MinIO simulation
s3_client = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",  # Using container name for MinIO
    aws_access_key_id="admin",
    aws_secret_access_key="admin123",
    config=Config(signature_version="s3v4"),
)

def create_bucket(bucket_name="netopsx-bucket"):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully!")
    except Exception as e:
        print(f"Bucket creation error (possibly already exists): {e}")

def upload_sample_file(bucket_name="netopsx-bucket", file_path="sample.txt"):
    try:
        s3_client.upload_file(file_path, bucket_name, "sample.txt")
        print("File uploaded to MinIO successfully!")
    except Exception as e:
        print("Error uploading file:", e)

def create_dynamodb_table():
    # Use dummy credentials since DynamoDB Local doesn't require real ones.
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://dynamodb:8000",
        region_name="us-east-1",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy"
    )
    try:
        table = dynamodb.create_table(
            TableName="Transactions",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Transactions")
        print("DynamoDB table 'Transactions' created locally!")
    except Exception as e:
        print("Error creating DynamoDB table (it may already exist):", e)
