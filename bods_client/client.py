"""
client.py a module containing a client for requesting data from the BODS API.
"""
import json
from typing import Optional, Union

import requests
from google.transit.gtfs_realtime_pb2 import FeedMessage

from bods_client.constants import (
    OK_200,
    V1_FARES_URL,
    V1_GTFS_RT_URL,
    V1_SIRI_VM_URL,
    V1_TIMETABLES_URL,
)
from bods_client.models import (
    APIError,
    Fares,
    FaresResponse,
    Timetable,
    TimetableParams,
    TimetableResponse,
)
from bods_client.models.avl import GTFSRTParams, SIRIVMParams
from bods_client.models.fares import FaresParams


class BODSClient:
    """
    Client for requesting data from the BODS API.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _make_request(self, path: str, *args, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = 60

        if "params" in kwargs:
            kwargs["params"]["api_key"] = self.api_key
        else:
            kwargs["params"] = {"api_key": self.api_key}

        return requests.get(path, *args, **kwargs)

    def get_timetable_datasets(
        self, params: Optional[TimetableParams] = None
    ) -> Union[TimetableResponse, APIError]:
        """
        Fetches the data sets currently available in the BODS database.

        This only returns meta data about a data set including a url to
        the actual data set.

        Args:
            admin_areas: A list of NPTG ATCO Area codes.
            nocs: A list of National Operator Codes.
            status: Limit data sets with a specific status of published, error, expired,
            inactive.
            search: Return data sets with search term in the data set name, data set.
            description, organisation name, or admin name.
            modified_date: Get data sets created/updated after this date.
            start_date_start: Limit data sets to those with start dates after this date.
            start_date_end: Limit date sets to those with start dates before this date.
            end_date_start: Get data sets with end dates after this date.
            end_date_end: Get data sets with end dates before this date.
            limit: Maximum number of results to return per page.
            offset: Number to offset results by.
        """

        if params is None:
            params = TimetableParams()

        params = json.loads(params.json(by_alias=True, exclude_none=True))
        response = self._make_request(V1_TIMETABLES_URL, params=params)

        if response.status_code == OK_200:
            return TimetableResponse(**response.json())
        return APIError(status_code=response.status_code, reason=response.content)

    def get_timetable_dataset(
        self, dataset_id: int
    ) -> Union[TimetableResponse, APIError]:
        """
        Get a single timetable dataset.

        Args:
            dataset_id: The id of the timetable data set.

        Returns:
            timetable: A Timetable object with the data set details.
        """

        url = V1_TIMETABLES_URL + f"/{dataset_id}"
        response = self._make_request(url)

        if response.status_code == 200:
            results = [Timetable(**response.json())]
            return TimetableResponse(count=1, results=results)

        return APIError(status_code=response.status_code, reason=response.content)

    def get_fares_datasets(
        self,
        params: Optional[FaresParams] = None,
    ) -> Union[FaresResponse, APIError]:
        """
        Fetches the fares data sets currently available in the BODS database.

        This only returns meta data about a fares data set including a url to
        the actual data set.

        Args:
            nocs: A list of National Operator Codes.
            status: Limit data sets with a specific status of published, error, expired,
            inactive.
            bounding_box: Limit data sets to those within the BoundingBox.
            limit: Maximum number of results to return per page.
            offset: Number to offset results by.

        """
        if params is None:
            params = FaresParams()

        params = json.loads(params.json(by_alias=True, exclude_none=True))
        response = self._make_request(V1_FARES_URL, params=params)
        if response.status_code == 200:
            return FaresResponse(**response.json())
        return APIError(status_code=response.status_code, reason=response.content)

    def get_fares_dataset(self, dataset_id: int) -> Union[FaresResponse, APIError]:
        """
        Fetches a single fares data sets currently available in the BODS database.
        """
        url = V1_FARES_URL + f"/{dataset_id}"
        response = self._make_request(url)
        if response.status_code == 200:
            results = [Fares(**response.json())]
            return FaresResponse(count=1, results=results)
        return APIError(status_code=response.status_code, reason=response.content)

    def get_siri_vm_data_feed(
        self,
        params: Optional[SIRIVMParams] = None,
    ) -> Union[bytes, APIError]:
        """
        Returns a SIRI-VM byte string representation of vehicles currently providing an
        Automatic Vehicle Locations in BODS.

        Args:
            bounding_box: Limit vehicles to those within the BoundingBox.
            operator_refs: Limit vehicles to only certain operators.
            line_ref: Limit vehicles to those on a certain line.
            producer_ref: Limit vehicles to created by a certain producer.
            origin_ref: Limit vehicles to those with a certain origin.
            destinaton_ref: Limit vehicles to those heading for a certain destination.
        """

        if params is None:
            params = SIRIVMParams()

        params = json.loads(params.json(by_alias=True, exclude_none=True))
        response = self._make_request(V1_SIRI_VM_URL, params=params)
        if response.status_code == OK_200:
            return response.content
        return APIError(status_code=response.status_code, reason=response.content)

    def get_gtfs_rt_data_feed(
            self, params: Optional[GTFSRTParams] = None
    ) -> Union[FeedMessage, APIError]:

        """
        Returns a FeedMessage of vehicles currently providing Automatic Vehicle
        Locations in BODS.

        Args:
            bounding_box: Limit vehicles to those within the BoundingBox.
            route_id: Limit vehicles to those with this route id.
            start_time_after: Limit vehicles to those with start time after this
            datetime.
            start_time_before: Limit vehicles to with the start time before this
            datetime.
        """
        if params is None:
            params = GTFSRTParams()

        params = json.loads(params.json(by_alias=True, exclude_none=True))
        response = self._make_request(V1_GTFS_RT_URL, params=params)
        if response.status_code == OK_200:
            message = FeedMessage()
            message.ParseFromString(response.content)
            return message
        return APIError(status_code=response.status_code, reason=response.content)
