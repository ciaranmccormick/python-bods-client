"""
client.py a module containing a client for requesting data from the BODS API.
"""
from datetime import datetime
from typing import Dict, List, Optional, Union
from google.transit.gtfs_realtime_pb2 import FeedMessage

import requests

from bods_client.constants import (
    DATASET_STATUSES,
    DATETIME_FORMAT,
    OK_200,
    V1_FARES_URL,
    V1_GTFS_RT_URL,
    V1_TIMETABLES_URL,
)
from bods_client.models import APIError, APIResponse, Fare, Timetable, BoundingBox
from bods_client.types import AdminAreasType, NOCs

Params = Dict[str, Union[str, int, List[str], AdminAreasType, NOCs, List[float]]]


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
        self,
        admin_areas: Optional[AdminAreasType] = None,
        nocs: Optional[NOCs] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        modified_date: Optional[datetime] = None,
        start_date_start: Optional[datetime] = None,
        start_date_end: Optional[datetime] = None,
        end_date_start: Optional[datetime] = None,
        end_date_end: Optional[datetime] = None,
        limit: int = 25,
        offset: int = 0,
    ) -> Union[APIResponse, APIError]:
        """Fetches the data sets currently available in the BODS database.

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
        params: Params = {"offset": offset, "limit": limit}

        if admin_areas:
            params["adminAreas"] = admin_areas

        if nocs:
            params["noc"] = nocs

        if status:
            assert (
                status in DATASET_STATUSES
            ), f"`status` must be one of {','.join(DATASET_STATUSES)}"
            params["status"] = status

        if search:
            params["search"] = search

        if modified_date:
            params["modifiedDate"] = modified_date.strftime(DATETIME_FORMAT)

        if start_date_start:
            params["startDateStart"] = start_date_start.strftime(DATETIME_FORMAT)

        if start_date_end:
            params["startDateEnd"] = start_date_end.strftime(DATETIME_FORMAT)

        if end_date_start:
            params["endDateStart"] = end_date_start.strftime(DATETIME_FORMAT)

        if end_date_end:
            params["endDateEnd"] = end_date_end.strftime(DATETIME_FORMAT)

        response = self._make_request(V1_TIMETABLES_URL, params=params)
        if response.status_code == OK_200:
            return APIResponse(**response.json())

        return APIError(status_code=response.status_code, reason=response.content)

    def get_timetable_dataset(self, dataset_id: int) -> Union[APIResponse, APIError]:
        """Get a single timetable dataset.

        Args:
            dataset_id: The id of the timetable data set.

        Returns:
            timetable: A Timetable object with the data set details.
        """

        url = V1_TIMETABLES_URL + f"/{dataset_id}"
        response = self._make_request(url)
        if response.status_code == 200:
            results = [Timetable(**response.json())]
            return APIResponse(count=1, results=results)
        return APIError(status_codes=response.status_code, reason=response.content)

    def get_fare_datasets(
        self,
        nocs: Optional[NOCs] = None,
        status: Optional[str] = None,
        bounding_box: Optional[BoundingBox] = None,
        limit: int = 25,
        offset: int = 0,
    ):
        params: Params = {"limit": limit, "offset": offset}

        if nocs:
            params["noc"] = nocs

        if status:
            assert (
                status in DATASET_STATUSES
            ), f"`status` must be one of {','.join(DATASET_STATUSES)}"
            params["status"] = status

        if bounding_box:
            params["boundingBox"] = bounding_box.list()

        response = self._make_request(V1_FARES_URL, params=params)

        if response.status_code == 200:
            return APIResponse(**response.json())
        return APIError(status=response.status_code, reason=response.content)

    def get_fare_dataset(self, dataset_id: int) -> Union[APIResponse, APIError]:
        url = V1_FARES_URL + f"/{dataset_id}"
        response = self._make_request(url)
        if response.status_code == 200:
            results = [Fare(**response.json())]
            return APIResponse(count=1, results=results)
        return APIError(status_codes=response.status_code, reason=response.content)

    def get_gtfs_rt_data_feed(
        self,
        bounding_box: Optional[BoundingBox] = None,
        route_id: Optional[str] = None,
        start_time_after: Optional[datetime] = None,
        start_time_before: Optional[datetime] = None,
    ) -> Union[FeedMessage, APIError]:

        params: Params = {}
        if bounding_box:
            params["boundingBox"] = bounding_box.csv()

        if route_id:
            params["routeId"] = route_id

        if start_time_after and start_time_before:
            raise ValueError(
                "Only one of 'start_time_after' or 'start_time_before' "
                "should be specified."
            )

        if start_time_after:
            params["startTimeAfter"] = int(start_time_after.timestamp())

        if start_time_before:
            params["startTimeBefore"] = int(start_time_before.timestamp())

        response = self._make_request(V1_GTFS_RT_URL, params=params)
        if response.status_code == OK_200:
            message = FeedMessage()
            message.ParseFromString(response.content)
            return message
        return APIError(status_codes=response.status_code, reason=response.text)
