from pydantic import BaseModel


# Schema for returning token data
class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str