from typing import List, Optional
import boto3
import os
import json
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from pydantic import BaseModel, Field

tracer = Tracer()
logger = Logger(log_uncaught_exceptions=True)

sns = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table()
TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")

MAX_STR_INPUT_LENGTH = 1000000
SAFE_STR_REGEX = r"^[A-Za-z0-9-_. ]*$"
SAFE_SHORT_STR_VALIDATION = Field(min_length=0, max_length=500, pattern=SAFE_STR_REGEX)


class ModelKwargsFieldValidation(BaseModel):
    streaming: Optional[bool]
    maxTokens: Optional[int] = Field(gt=0, lt=1000000)
    temperature: Optional[float] = Field(ge=0, le=1)
    topP: Optional[float] = Field(ge=0, le=1)


class FileFieldValidation(BaseModel):
    provider: Optional[str] = SAFE_SHORT_STR_VALIDATION
    key: Optional[str] = SAFE_SHORT_STR_VALIDATION


class DataFieldValidation(BaseModel):
    modelName: Optional[str] = SAFE_SHORT_STR_VALIDATION
    provider: Optional[str] = SAFE_SHORT_STR_VALIDATION
    sessionId: Optional[str] = SAFE_SHORT_STR_VALIDATION
    workspaceId: Optional[str] = SAFE_SHORT_STR_VALIDATION
    mode: Optional[str] = SAFE_SHORT_STR_VALIDATION
    text: Optional[str] = Field(min_length=1, max_length=MAX_STR_INPUT_LENGTH)
    files: Optional[List[FileFieldValidation]]
    modelKwargs: Optional[ModelKwargsFieldValidation]


class InputValidation(BaseModel):
    action: str = SAFE_SHORT_STR_VALIDATION
    modelInterface: str = SAFE_SHORT_STR_VALIDATION
    data: DataFieldValidation


@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    log_event=False, correlation_id_path=correlation_paths.APPSYNC_RESOLVER
)
def handler(event, context: LambdaContext):
    # input logger info that will print all event and context

    logger.info(f"event: {event}")
    # logger.info(f"context: {context}")
    body = json.loads(event["body"])
    logger.info(f"body: {body}")
    request = json.loads(body["arguments"]["data"])
    
    logger.info(f"request: {request}")

    try:
        sessionId = request["data"]["sessionId"]
        logger.info(f"session-id: {sessionId}")
    except Exception as e:
        logger.error("error on parsing sessionId")


    # request = json.loads(event["arguments"]["data"])

    

    message = {
        "action": request["action"],
        "modelInterface": request["modelInterface"],
        "direction": "IN",
        "timestamp": str(int(round(datetime.now().timestamp()))),
        # "userId": event["identity"]["sub"],
        "userId":"unicorn",
        "data": request.get("data", {}),
    }
    InputValidation(**message)

    try:
        response = sns.publish(TopicArn=TOPIC_ARN, Message=json.dumps(message))
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }
        # return response
    except Exception as e:
        # Do not return an unknown exception to the end user.
        logger.exception(e)
        raise RuntimeError("Something went wrong")
