from pydantic import BaseModel, Field, RootModel
from typing import List, Optional


class Translation(BaseModel):
    en: Optional[str]
    se: Optional[str]
    no: Optional[str]


class SameAsLocation(BaseModel):
    en: Optional[str]
    no: Optional[str]
    se: Optional[str]
    sameAs: Optional[List[str]] = []
    latitude: Optional[str]
    longitude: Optional[str]


class Place(BaseModel):
    city: Optional[Translation]
    country: Optional[Translation]
    cityNow: Optional[SameAsLocation]
    countryNow: Optional[SameAsLocation]
    continent: Optional[Translation]
    locationString: Optional[Translation]


class Birth(BaseModel):
    date: Optional[str]
    year: Optional[str]
    place: Optional[Place]


class Wikipedia(BaseModel):
    slug: Optional[str]
    english: Optional[str]


class Wikidata(BaseModel):
    id: Optional[str]
    url: Optional[str]


class Link(BaseModel):
    rel: Optional[str]
    href: Optional[str]
    action: Optional[str]
    types: Optional[str]
    title: Optional[str]
    class_: Optional[List[str]] = Field(default=None, alias="class")


class Category(BaseModel):
    en: Optional[str]
    no: Optional[str]
    se: Optional[str]


class Motivation(BaseModel):
    en: Optional[str]
    se: Optional[str]


class Affiliation(BaseModel):
    name: Optional[Translation]
    nameNow: Optional[Translation]
    city: Optional[Translation]
    country: Optional[Translation]
    cityNow: Optional[SameAsLocation]
    countryNow: Optional[SameAsLocation]
    continent: Optional[Translation]
    locationString: Optional[Translation]


class NobelPrize(BaseModel):
    awardYear: Optional[str]
    category: Optional[Category]
    categoryFullName: Optional[Category]
    sortOrder: Optional[str]
    portion: Optional[str]
    dateAwarded: Optional[str]
    prizeStatus: Optional[str]
    motivation: Optional[Motivation]
    prizeAmount: Optional[int]
    prizeAmountAdjusted: Optional[int]
    affiliations: Optional[List[Affiliation]] = []
    links: Optional[List[Link]] = []


class Laureate(BaseModel):
    id: Optional[str]
    knownName: Optional[Translation]
    givenName: Optional[Translation]
    familyName: Optional[Translation]
    fullName: Optional[Translation]
    fileName: Optional[str]
    gender: Optional[str]
    birth: Optional[Birth]
    wikipedia: Optional[Wikipedia]
    wikidata: Optional[Wikidata]
    sameAs: Optional[List[str]] = []
    links: Optional[List[Link]] = []
    nobelPrizes: Optional[List[NobelPrize]] = []


class Meta(BaseModel):
    offset: Optional[int]
    limit: Optional[int]
    count: Optional[int]
    terms: Optional[str]
    license: Optional[str]
    disclaimer: Optional[str]


class PaginationLinks(BaseModel):
    first: Optional[str]
    self: Optional[str]
    next: Optional[str]
    last: Optional[str]


class LaureateResponse(BaseModel):
    laureates: List[Laureate]
    meta: Optional[Meta]
    links: Optional[PaginationLinks]


class LaureateIdResponse(Laureate):
    meta: Optional[Meta]

class LaureateIdListResponse(RootModel[list[LaureateIdResponse]]):
    pass