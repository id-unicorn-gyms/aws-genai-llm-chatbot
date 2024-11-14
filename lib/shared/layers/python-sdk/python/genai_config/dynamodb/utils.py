import boto3
from typing import Any, Dict

def get_dynamodb_client():
    return boto3.client('dynamodb')

def read_key_value_from_dynamodb(table_name: str, key_name: str, key_value: Any) -> Any:
    """
    Read a key-value pair from AWS DynamoDB.
    
    :param table_name: The name of the DynamoDB table
    :param key_name: The name of the key in the table
    :param key_value: The value of the key to search for
    :return: The value associated with the key, or None if not found
    """
    dynamodb = get_dynamodb_client()
    
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                key_name: {'S': str(key_value)}
            }
        )
        
        if 'Item' in response:
            # print(response['Item'])
            return response['Item']
        else:
            return None
    except Exception as e:
        print(f"Error reading from DynamoDB: {str(e)}")
        return None