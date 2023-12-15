from schema import USER_SCHEMA_CLASS, ADV_SCHEMA_CLASS
from pydantic import ValidationError
from errors import HttpError




def validate_user(schema_cls: USER_SCHEMA_CLASS, json_data: dict | list):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise HttpError(400, error)


def validate_advertisement(schema_cls: ADV_SCHEMA_CLASS, json_data: dict | list):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise HttpError(400, error)

