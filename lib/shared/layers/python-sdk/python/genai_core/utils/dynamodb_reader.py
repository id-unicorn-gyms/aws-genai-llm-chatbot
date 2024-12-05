import boto3
from typing import Any

dynamodb_client = boto3.client("dynamodb")

def read_key_value_from_dynamodb(table_name: str, key_name: str, key_value: Any) -> Any:
    """
    Read a key-value pair from AWS DynamoDB.

    :param table_name: The name of the DynamoDB table
    :param key_name: The name of the key in the table
    :param key_value: The value of the key to search for
    :return: The value associated with the key, or None if not found
    """

    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={
                key_name: {'S': str(key_value)}
            }
        )

        if 'Item' in response:
            return response['Item']
        else:
            return None
    except Exception as e:
        print(f"Error reading from DynamoDB: {str(e)}")
        return None


class DynamoDBReader:
    def __init__(self, table_name: str, key_name: str):
        self.table_name = table_name
        self.key_name = key_name

    def read_value(self, key_value: Any) -> Any:
        return read_key_value_from_dynamodb(self.table_name, self.key_name, key_value)

    def get_override_prompt_template(self, provider, model_id):
        item = self.read_value(f"{provider}.{model_id}")
        return {
        "prompt": item["prompt"]["S"] if item and item.get("prompt") else None,
        "prompt_qna": item["prompt_qna"]["S"] if item and item.get("prompt_qna") else None,
        "prompt_condensed_qna": item["prompt_condensed_qna"]["S"] if item and item.get("prompt_condensed_qna") else None,
        }
