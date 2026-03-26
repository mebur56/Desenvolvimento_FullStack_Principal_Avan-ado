from pydantic import BaseModel, RootModel, Field
from enum import Enum

class DefaultResponse(BaseModel):
    message: str

class FavoriteItem(BaseModel):
    id: int
    laureateId: int
    laureateName: str
    amount: int
    motivation: str
    description: str

class FavoriteItemResponse(RootModel[list[FavoriteItem]]):
    pass    

class FavoriteInput(BaseModel):
    laureateId: int = Field(example=1)
    description: str= Field(example="Relacionado a minha área de estudo")

class FavoriteEditInput(BaseModel):
    id: int = Field(example=1)
    description: str= Field(example="Relacionado a minha área de estudo")
class FavoriteIdQuery(BaseModel):
    id: int 


class OrderByEnum(str, Enum):
    amount = "amount"
    name = "name"
class FavoriteDetailsQuery(BaseModel):
    orderBy: OrderByEnum    