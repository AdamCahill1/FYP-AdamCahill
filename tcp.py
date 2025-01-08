import socket
import struct
import boto3
from datetime import datetime


dynamodb = boto3.resource('dynamodb')
table_name = "mileageData"
table = dynamodb.Table(table_name)



def upload_to_dynamodb(vin, mileage):
    try:
        table.put_item(
            Item={
                'vin': vin,
                'mileage (meters)': mileage,  
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        print(f"Uploaded to DynamoDB")
    except Exception as e:
        print(f"Error uploading to DynamoDB: {e}")



def tcp_client():
    host = "127.0.0.1"  
    port = 40001        

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while True:
        data = client_socket.recv(22)
        if not data:
            break
        
        # https://docs.python.org/3/library/struct.html
        mileage = struct.unpack("@l", data[:4])[0]

        vin = data[4:21].decode('utf-8')

        print(f"Received: Mileage = {mileage / 1000.0:.2f}, VIN = {vin}")

        upload_to_dynamodb(vin, mileage)
        
    client_socket.close()
    print("Disconnected from server.")

if __name__ == "__main__":
    tcp_client()
