# create a class that call dynamodb/utils.py to read value from key
from typing import Any
from genai_config.dynamodb.utils import read_key_value_from_dynamodb

class DynamoDBReader:
    def __init__(self, table_name: str, key_name: str):
        self.table_name = table_name
        self.key_name = key_name

    def read_value(self, key_value: Any) -> Any:
        return read_key_value_from_dynamodb(self.table_name, self.key_name, key_value)