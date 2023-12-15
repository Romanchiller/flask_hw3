import pydantic
import re
from typing import Optional, Type


class AbstractUser(pydantic.BaseModel):
    name: str
    password: str
    e_mail: str

    @pydantic.field_validator('name')
    @classmethod
    def name_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError('Максимальная длина имени 100')
        return v

    @pydantic.field_validator('password')
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Минимальная  длина пароля 8')
        return v

    @pydantic.field_validator('e_mail')
    @classmethod
    def e_mail_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError('Максимальная длина e_mail 100')
        return v

    @pydantic.field_validator('e_mail')
    @classmethod
    def e_mail_correct(cls, v: str) -> str:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'
        result = re.search(pattern, v)
        if result is None:
            raise ValueError('Not correct e_mail')
        return v


class CreateUser(AbstractUser):
    name: str
    password: str
    e_mail: Optional[str] = None


class UpdateUser(AbstractUser):
    name: Optional[str] = None
    password: Optional[str] = None
    e_mail: Optional[str] = None


class AbstractAdvertisements(pydantic.BaseModel):
    header: str
    description: str
    author: int

    @pydantic.field_validator('header')
    @classmethod
    def header_length(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError('Максимальная длина имени 200')
        return v


class CreateAdvertisement(AbstractAdvertisements):
    header: str
    description: str



class UpdateAdvertisement(AbstractAdvertisements):
    header: Optional[str] = None
    description: Optional[str] = None


USER_SCHEMA_CLASS = Type[CreateUser | UpdateUser]
USER_SCHEMA = CreateUser | UpdateUser


ADV_SCHEMA_CLASS = Type[CreateAdvertisement | UpdateAdvertisement]
ADV_SCHEMA = CreateAdvertisement | UpdateAdvertisement
