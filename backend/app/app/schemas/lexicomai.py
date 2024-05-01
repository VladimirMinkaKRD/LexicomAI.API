from app.schemas.base import BaseSchema


class BaseLexicomAI(BaseSchema):
    phone: str
    address: str


class CreatingLexicomAI(BaseLexicomAI):
    ...

class UpdatingLexicomAI(BaseLexicomAI):
    ...
