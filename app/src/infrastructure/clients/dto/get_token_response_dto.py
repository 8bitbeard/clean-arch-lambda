from pydantic import BaseModel


class GetTokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    type: str
    scopes: str
