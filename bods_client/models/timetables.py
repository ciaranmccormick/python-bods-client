from datetime import datetime
from typing import List, Optional

from pydantic.fields import Field

from bods_client.models.base import (
    AdminAreas,
    BaseAPIParams,
    BaseAPIResponse,
    BaseDataset,
    Locality,
)
from bods_client.types import AdminAreasType


class Timetable(BaseDataset):
    lines: List[str]
    localities: List[Locality]
    admin_areas: List[AdminAreas] = Field(alias="adminAreas")
    first_start_date: datetime = Field(alias="firstStartDate")
    first_end_date: datetime = Field(None, alias="firstEndDate")
    last_end_date: datetime = Field(None, alias="lastEndDate")
    dq_score: str = Field(alias="dqScore")
    dq_rag: str = Field(alias="dqRag")
    bods_compliance: bool = Field(None, alias="bodsCompliance")


class TimetableParams(BaseAPIParams):
    class Config(BaseAPIParams.Config):
        pass

    admin_areas: Optional[AdminAreasType] = Field(None, alias="adminAreas")
    search: Optional[str] = None
    modified_date: Optional[datetime] = Field(None, alias="modifiedDate")
    start_date_start: Optional[datetime] = Field(None, alias="startDateEnd")
    start_date_end: Optional[datetime] = Field(None, alias="startDateStart")
    end_date_start: Optional[datetime] = Field(None, alias="endDateStart")
    end_date_end: Optional[datetime] = Field(None, alias="endDateEnd")
    dq_rag: Optional[str] = Field(None, alias="dqRag")
    bods_compliance: Optional[bool] = Field(None, alias="bodsCompliance")


class TimetableResponse(BaseAPIResponse):
    results: List[Timetable]
