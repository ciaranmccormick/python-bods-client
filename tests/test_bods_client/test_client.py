from bods_client.models.avl import GTFSRTParams, SIRIVMParams
from bods_client.models.base import BoundingBox
from bods_client.models.fares import FaresParams
from bods_client.models.timetables import TimetableParams
from bods_client.constants import V1_FARES_URL, V1_GTFS_RT_URL, V1_SIRI_VM_URL, V1_TIMETABLES_URL
from unittest.mock import MagicMock, patch
import pytest

from requests import Response

from bods_client.client import BODSClient


@patch("bods_client.client.requests")
def test_client_make_request(mrequests):
    key = "apikey"
    url = "http://fakeurl.url/"
    client = BODSClient(api_key=key)
    client._make_request(url)
    mrequests.get.assert_called_once_with(url, timeout=60, params={"api_key": key})


@patch("bods_client.client.requests")
def test_client_make_request_with_timeout(mrequests):
    key = "apikey"
    url = "http://fakeurl.url/"
    client = BODSClient(api_key=key)
    client._make_request(url, timeout=40)
    mrequests.get.assert_called_once_with(url, timeout=40, params={"api_key": key})


@patch("bods_client.client.requests")
def test_client_make_request_with_params(mrequests):
    key = "apikey"
    url = "http://fakeurl.url/"
    params = {"operatorRef": "NT"}
    client = BODSClient(api_key=key)
    client._make_request(url, params=params)

    expected_params = dict(params)
    expected_params["api_key"] = key
    mrequests.get.assert_called_once_with(url, timeout=60, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_timetable_datasets_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_timetable_datasets()

    expected_params = {"limit": 25, "offset": 0}
    mrequests.assert_called_once_with(V1_TIMETABLES_URL, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_timetable_datasets_with_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    params = TimetableParams(limit=10, nocs=["NT"])
    client.get_timetable_datasets(params=params)

    expected_params = {"limit": 10, "offset": 0, "noc": ["NT"]}
    mrequests.assert_called_once_with(V1_TIMETABLES_URL, params=expected_params)


@pytest.mark.parametrize(
    ("id_", "method", "expected_url"),
    [
        (5, "get_timetable_dataset", V1_TIMETABLES_URL + "/5"),
        (5, "get_fares_dataset", V1_FARES_URL + "/5"),
    ],
)
@patch("bods_client.client.BODSClient._make_request")
def test_get_dataset(mrequests, id_, method, expected_url):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    getattr(client, method)(dataset_id=id_)
    mrequests.assert_called_once_with(expected_url)


@patch("bods_client.client.BODSClient._make_request")
def test_get_fares_datasets_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_fares_datasets()

    expected_params = {"limit": 25, "offset": 0}
    mrequests.assert_called_once_with(V1_FARES_URL, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_fares_datasets_bounding_box(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    bb = {
        "min_longitude": -0.542423,
        "min_latitude": 51.267729,
        "max_longitude": 0.277432,
        "max_latitude": 51.753191,
    }
    bounding_box = BoundingBox(**bb)
    params = FaresParams(limit=10, bounding_box=bounding_box)
    client.get_fares_datasets(params=params)

    expected_params = {"limit": 10, "offset": 0, "boundingBox": bounding_box.csv()}
    mrequests.assert_called_once_with(V1_FARES_URL, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_siri_vm_bounding_box(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    bb = {
        "min_longitude": -0.542423,
        "min_latitude": 51.267729,
        "max_longitude": 0.277432,
        "max_latitude": 51.753191,
    }
    bounding_box = BoundingBox(**bb)
    params = SIRIVMParams(bounding_box=bounding_box)
    client.get_siri_vm_data_feed(params=params)
    expected_params = {"boundingBox": bounding_box.csv()}
    mrequests.assert_called_once_with(V1_SIRI_VM_URL, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_siri_vm_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response
    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_siri_vm_data_feed()
    mrequests.assert_called_once_with(V1_SIRI_VM_URL, params={})


@patch("bods_client.client.BODSClient._make_request")
def test_get_gtfs_rt_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response
    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_gtfs_rt_data_feed()
    mrequests.assert_called_once_with(V1_GTFS_RT_URL, params={})


@patch("bods_client.client.BODSClient._make_request")
def test_get_gtfs_rt_bounding_box(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    bb = {
        "min_longitude": -0.542423,
        "min_latitude": 51.267729,
        "max_longitude": 0.277432,
        "max_latitude": 51.753191,
    }
    bounding_box = BoundingBox(**bb)
    params = GTFSRTParams(bounding_box=bounding_box, route_id="51")
    client.get_gtfs_rt_data_feed(params=params)
    expected_params = {"boundingBox": bounding_box.csv(), "routeId": "51"}
    mrequests.assert_called_once_with(V1_GTFS_RT_URL, params=expected_params)

