import os
import boto3
import genai_core.workspaces
import genai_core.types
import unicodedata
from botocore.config import Config

UPLOAD_BUCKET_NAME = os.environ.get("UPLOAD_BUCKET_NAME")
USE_S3_ACCELERATE_ENDPOINT = os.environ.get("USE_S3_ACCELERATE_ENDPOINT", "false") == "true"
MAX_FILE_SIZE = 100 * 1000 * 1000  # 100Mb

s3_client = boto3.client("s3", region_name = os.environ['AWS_REGION'], config = Config(signature_version = 's3v4', s3={'addressing_style': 'virtual'}))


def generate_presigned_post(workspace_id: str, file_name: str, expiration=3600):

    file_name = unicodedata.normalize("NFC", file_name)
    workspace = genai_core.workspaces.get_workspace(workspace_id)
    if not workspace:
        raise genai_core.types.CommonError("Workspace not found")

    file_name = os.path.basename(file_name)
    object_name = f"{workspace_id}/{file_name}"

    conditions = [
        ["content-length-range", 0, MAX_FILE_SIZE],
    ]

    response = s3_client.generate_presigned_post(
        UPLOAD_BUCKET_NAME, object_name, Conditions=conditions, ExpiresIn=expiration
    )

    if not response:
        return None

    if USE_S3_ACCELERATE_ENDPOINT:
        response["url"] = f"https://{UPLOAD_BUCKET_NAME}.s3-accelerate.amazonaws.com"

    return response
