from pydantic import BaseModel


class SecretDTO(BaseModel):
    client_id: str
    client_secret: str
