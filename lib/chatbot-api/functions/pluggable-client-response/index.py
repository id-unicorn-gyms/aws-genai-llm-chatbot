import boto3
from aws_lambda_powertools import Logger, Tracer
from botocore.exceptions import ClientError
import os
import json

logger = Logger()

AWS_REGION = os.environ["AWS_REGION"]

SESSIONS_TABLE_NAME = os.environ["SESSIONS_TABLE_NAME"]
SESSIONS_BY_USER_ID_INDEX_NAME = os.environ["SESSIONS_BY_USER_ID_INDEX_NAME"]

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(SESSIONS_TABLE_NAME)
logger = Logger()


def get_session(session_id, user_id):
    response = {}
    try:
        response = table.get_item(Key={"SessionId": session_id, "UserId": user_id})
    except ClientError as error:
        if error.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.warning("No record found with session id: %s", session_id)
        else:
            logger.exception(error)

    return response.get("Item", {})

def handler(event, context):

    if event.get('httpMethod', '') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',  # Allow specific methods
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',  # Allow specific headers
            },
            'body': json.dumps('Preflight response')
        }

    logger.info(f"event: {event}")

    data = json.loads(event["body"])

    session_id = data["sessionId"]
    user_id = data["userId"]

    logger.info(f"userId {user_id}")
    logger.info(f"sessionId {session_id}")

    sessions = get_session(session_id,user_id)
    last_history = sessions["History"][-1]["data"]["content"]

    # TODO implement
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
        'body': json.dumps({"AI": last_history})
    }

    return response
