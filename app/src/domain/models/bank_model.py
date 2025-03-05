from pydantic import BaseModel


class BankModel(BaseModel):
    id: str
    name: str
    ispb: str
