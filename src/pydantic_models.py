from pydantic import BaseModel, RootModel, Field
from enum import Enum
from typing import List, Optional, Dict

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

class NobelQuery(BaseModel):
    category: str
    year: int

class OrderByEnum(str, Enum):
    amount = "amount"
    name = "name"
class FavoriteDetailsQuery(BaseModel):
    orderBy: OrderByEnum    



class TranslatedText(BaseModel):
    en: Optional[str] = None
    no: Optional[str] = None
    se: Optional[str] = None
    
class LaureateParams(BaseModel):
    ids: List[int] = Field(..., description="Lista de IDs dos laureados")

class Link(BaseModel):
    rel: str
    href: str
    action: str
    types: str


class Laureate(BaseModel):
    id: str
    knownName: Dict[str, str]
    fullName: Dict[str, str]
    motivation: Dict[str, str]


class NobelPrize(BaseModel):
    awardYear: str
    category: TranslatedText
    categoryFullName: TranslatedText
    dateAwarded: str
    prizeAmount: int
    prizeAmountAdjusted: int
    laureates: List[Laureate]

class NobelResponse(BaseModel):
    nobelPrizes: List[NobelPrize]
