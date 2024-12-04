from pydantic import Field


MAX_STR_INPUT_LENGTH = 1000000
SAFE_STR_REGEX = r"^[A-Za-z0-9-_.\/ ]*$"
SAFE_HTTP_STR_REGEX = r"^[A-Za-z0-9-_.:/]*$"
ID_FIELD_VALIDATION = Field(min_length=1, max_length=100, pattern=SAFE_STR_REGEX)
SAFE_SHORT_STR_VALIDATION = Field(min_length=1, max_length=100, pattern=SAFE_STR_REGEX)
MODEL_NAME_SAFE_STR_REGEX = r"^[A-Za-z0-9-_.]*(:[0-9]+)?$"
MODEL_NAME_SAFE_SHORT_STR_VALIDATION = Field(min_length=0, max_length=500, pattern=MODEL_NAME_SAFE_STR_REGEX)
FILE_NAME_SAFE_STR_REGEX = r"^[A-Za-z0-9-_.\[\] ]*$"
FILE_NAME_SAFE_SHORT_STR_VALIDATION = Field(min_length=0, max_length=500, pattern=FILE_NAME_SAFE_STR_REGEX)
