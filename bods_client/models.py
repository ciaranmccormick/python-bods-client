"""models.py"""
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel
from pydantic.fields import Field


class APIError(BaseModel):
    status_code: int
    reason: str


class AdminAreas(BaseModel):
    atco_code: str
    name: str


class Locality(BaseModel):
    gazetteer_id: str
    name: str


class BaseDataset(BaseModel):
    id: int
    operator_name: str = Field(alias="operatorName")
    name: str
    description: str
    comment: str
    status: str
    nocs: List[str] = Field(alias="noc")
    created: datetime
    modified: datetime


class Timetable(BaseDataset):
    url: str
    lines: List[str]
    localities: List[Locality]
    admin_areas: List[AdminAreas] = Field(alias="adminAreas")
    first_start_date: datetime = Field(alias="firstStartDate")
    first_end_date: datetime = Field(alias="firstEndDate")
    last_end_date: datetime = Field(alias="lastEndDate")


class Fare(BaseDataset):
    URL: str = Field(alias="URL")
    num_of_lines: int = Field(alias="numOfLines")
    num_of_fare_zones: int = Field(alias="numOfFareZones")
    num_of_sales_offer_packages: int = Field(alias="numOfSalesOfferPackages")
    num_of_fare_products: int = Field(alias="numOfFareProducts")
    num_of_user_types: int = Field(alias="numOfUserTypes")


class APIResponse(BaseModel):
    count: int
    results: List[Union[Timetable, Fare]]
    next: Optional[str]
    previous: Optional[str]


class BoundingBox(BaseModel):
    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float

    def list(self) -> List[float]:
        return [
            self.min_longitude,
            self.min_latitude,
            self.max_longitude,
            self.max_latitude,
        ]

    def csv(self) -> str:
        return ",".join(str(f) for f in self.list())
