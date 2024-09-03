from datetime import datetime
from typing import Optional

from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.main import BaseModel

from bods_client.models.base import BoundingBoxMixin
from bods_client.types import NOCs


class BaseAVLParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class SIRIVMParams(BaseAVLParams, BoundingBoxMixin):
    operator_refs: Optional[NOCs] = Field(default=None, alias="operatorRef")
    line_ref: Optional[str] = Field(default=None, alias="lineRef")
    producer_ref: Optional[str] = Field(default=None, alias="producerRef")
    origin_ref: Optional[str] = Field(default=None, alias="originRef")
    destinaton_ref: Optional[str] = Field(default=None, alias="destinationRef")
    vehicle_ref: Optional[str] = Field(default=None, alias="vehicleRef")


class GTFSRTParams(BaseAVLParams, BoundingBoxMixin):
    route_id: Optional[str] = Field(default=None, alias="routeId")
    start_time_after: Optional[datetime] = Field(default=None, alias="startTimeAfter")
    start_time_before: Optional[datetime] = Field(default=None, alias="startTimeBefore")
