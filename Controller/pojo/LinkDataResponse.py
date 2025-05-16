from pydantic import BaseModel


class getLinkDataResponse(BaseModel):
    description: str
    price: str
