import json
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
    id: int
    created: datetime
    modified: datetime
    operator_name: str = Field(alias="operatorName")
    nocs: List[str] = Field(alias="noc")
    name: str
    description: str
    comment: str
    status: str
    url: str
    extension: str
    lines: List[str]
    first_start_date: datetime = Field(alias="firstStartDate")
    first_end_date: datetime = Field(default=None, alias="firstEndDate")
    last_end_date: datetime = Field(default=None, alias="lastEndDate")
    admin_areas: List[AdminAreas] = Field(alias="adminAreas")
    localities: List[Locality]
    dq_score: str = Field(alias="dqScore")
    dq_rag: str = Field(alias="dqRag")
    bods_compliance: Optional[bool] = Field(default=None, alias="bodsCompliance")


class TimetableParams(BaseAPIParams):
    admin_areas: Optional[AdminAreasType] = Field(default=None, alias="adminArea")
    search: Optional[str] = None
    modified_date: Optional[datetime] = Field(default=None, alias="modifiedDate")
    start_date_start: Optional[datetime] = Field(default=None, alias="startDateEnd")
    start_date_end: Optional[datetime] = Field(default=None, alias="startDateStart")
    end_date_start: Optional[datetime] = Field(default=None, alias="endDateStart")
    end_date_end: Optional[datetime] = Field(default=None, alias="endDateEnd")
    dq_rag: Optional[str] = Field(default=None, alias="dqRag")
    bods_compliance: Optional[bool] = Field(default=None, alias="bodsCompliance")

    def model_dump_json(self, *args, **kwargs):
        """Custom dict method to convert list of noc strings to a cvs.

        There's a bug in the BODS timetables API where ?noc=NOC1&noc=NOC2
        only recognises the last parameter. This also applies to adminArea too.
        """
        dict_ = super().model_dump(*args, **kwargs)

        if "noc" in dict_:
            dict_["noc"] = ",".join(dict_.get("noc", []))
        if "adminArea" in dict_:
            dict_["adminArea"] = ",".join(dict_.get("adminArea", []))
        return json.dumps(dict_)


class TimetableResponse(BaseAPIResponse):
    results: List[Timetable]
