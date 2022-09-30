from unittest.mock import MagicMock, patch

import pytest
from google.transit.gtfs_realtime_pb2 import FeedMessage
from requests import Response

from bods_client.client import BODSClient
from bods_client.constants import V1_FARES_URL, V1_TIMETABLES_URL
from bods_client.models.avl import GTFSRTParams, SIRIVMParams
from bods_client.models.base import APIError, BoundingBox
from bods_client.models.fares import FaresParams
from bods_client.models.timetables import TimetableParams


def test_url_with_trailing_slash():
    key = "apikey"
    url = "http://fakeurl.url/"
    client = BODSClient(api_key=key, base_url=url)
    assert client.base_url == url[:-1]


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
    mrequests.assert_called_once_with(client.timetable_endpoint, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_timetable_datasets_with_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    params = TimetableParams(limit=10, nocs=["NT", "PT"])
    client.get_timetable_datasets(params=params)

    expected_params = {"limit": 10, "offset": 0, "noc": "NT,PT"}
    mrequests.assert_called_once_with(client.timetable_endpoint, params=expected_params)


@pytest.mark.parametrize(
    ("id_", "method", "expected_url"),
    [
        (5, "get_timetable_dataset", V1_TIMETABLES_URL + "/5/"),
        (5, "get_fares_dataset", V1_FARES_URL + "/5/"),
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


def test_get_timetable_200(timetable_response):
    dataset_id = 5
    expected_url = V1_TIMETABLES_URL + f"/{dataset_id}/"

    key = "apikey"
    client = BODSClient(api_key=key)
    with patch("bods_client.client.BODSClient._make_request") as mrequests:
        mrequests.return_value = timetable_response
        client.get_timetable_dataset(dataset_id=dataset_id)
        mrequests.assert_called_once_with(expected_url)


def test_get_timetable_list_200(timetable_list_response):
    expected_url = V1_TIMETABLES_URL + "/"

    key = "apikey"
    client = BODSClient(api_key=key)
    with patch("bods_client.client.BODSClient._make_request") as mrequests:
        mrequests.return_value = timetable_list_response
        client.get_timetable_datasets()
        expected_params = {"limit": 25, "offset": 0}
        mrequests.assert_called_once_with(expected_url, params=expected_params)


def test_get_fare_200(fare_response):
    dataset_id = 5
    expected_url = V1_FARES_URL + f"/{dataset_id}/"

    key = "apikey"
    client = BODSClient(api_key=key)
    with patch("bods_client.client.BODSClient._make_request") as mrequests:
        mrequests.return_value = fare_response
        client.get_fares_dataset(dataset_id=dataset_id)
        mrequests.assert_called_once_with(expected_url)


def test_get_fare_list_200(fare_list_response):
    expected_url = V1_FARES_URL + "/"

    key = "apikey"
    client = BODSClient(api_key=key)
    with patch("bods_client.client.BODSClient._make_request") as mrequests:
        mrequests.return_value = fare_list_response
        client.get_fares_datasets()
        expected_params = {"limit": 25, "offset": 0}
        mrequests.assert_called_once_with(expected_url, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_fares_datasets_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response

    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_fares_datasets()

    expected_params = {"limit": 25, "offset": 0}
    mrequests.assert_called_once_with(client.fares_endpoint, params=expected_params)


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
    mrequests.assert_called_once_with(client.fares_endpoint, params=expected_params)


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
    mrequests.assert_called_once_with(client.siri_vm_endpoint, params=expected_params)


@patch("bods_client.client.BODSClient._make_request")
def test_get_siri_vm_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response
    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_siri_vm_data_feed()
    mrequests.assert_called_once_with(client.siri_vm_endpoint, params={})


@pytest.mark.usefixtures("_bods_requests")
def test_get_siri_vm_200_response():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    sirivm = client.get_siri_vm_data_feed()
    assert isinstance(sirivm, bytes)


@pytest.mark.usefixtures("_bods_requests")
def test_get_siri_vm_by_id_200_response():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    sirivm = client.get_siri_vm_data_feed_by_id(feed_id=10)
    assert isinstance(sirivm, bytes)


@pytest.mark.usefixtures("_bods_requests_error")
def test_get_siri_vm_by_id_non_200_response():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    sirivm = client.get_siri_vm_data_feed_by_id(feed_id=10)
    assert isinstance(sirivm, APIError)


@patch("bods_client.client.BODSClient._make_request")
def test_get_gtfs_rt_no_params(mrequests):
    response = MagicMock(spec=Response, status_code=400, content=b"Oopsie")
    mrequests.return_value = response
    key = "apikey"
    client = BODSClient(api_key=key)
    client.get_gtfs_rt_data_feed()
    mrequests.assert_called_once_with(client.gtfs_rt_endpoint, params={})


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
    mrequests.assert_called_once_with(client.gtfs_rt_endpoint, params=expected_params)


@pytest.mark.usefixtures("_bods_requests")
def test_siri_vm_from_archive_200():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    siri = client.get_siri_vm_from_archive()
    assert isinstance(siri, bytes)


@pytest.mark.usefixtures("_bods_requests_error")
def test_siri_vm_from_archive_error():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    siri = client.get_siri_vm_from_archive()
    assert isinstance(siri, APIError)


@pytest.mark.usefixtures("_bods_requests")
def test_gtfs_rt_from_archive_200():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    gtfsrt = client.get_gtfs_rt_from_archive()
    assert isinstance(gtfsrt, FeedMessage)


@pytest.mark.usefixtures("_bods_requests_error")
def test_gtfs_rt_from_archive_error():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    gtfsrt = client.get_gtfs_rt_from_archive()
    assert isinstance(gtfsrt, APIError)


@pytest.mark.usefixtures("_bods_requests")
def test_get_gtfsrt_200_response():
    api_key = "api_key"
    client = BODSClient(api_key=api_key)
    message = client.get_gtfs_rt_data_feed()
    assert isinstance(message, FeedMessage)
    assert len(message.entity) == 4
    assert message.header.gtfs_realtime_version == "2.0"
    assert message.header.timestamp == 1643658718
