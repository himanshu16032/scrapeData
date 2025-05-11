from pydantic import BaseModel


class getLinkDataResponse(BaseModel):
    description: str
    price: float
    name: str
    priceCurrency: str
    availability: str
