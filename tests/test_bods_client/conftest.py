import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from requests import Response

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture()
def timetable_response():
    timetable_path = DATA_DIR / "timetable.json"
    with timetable_path.open() as f:
        content = f.read()
        response = MagicMock(spec=Response, status_code=200, content=content)
        response.json.return_value = json.loads(content)
        yield response


@pytest.fixture()
def timetable_list_response():
    timetable_path = DATA_DIR / "timetables.json"
    with timetable_path.open() as f:
        content = f.read()
        response = MagicMock(spec=Response, status_code=200, content=content)
        response.json.return_value = json.loads(content)
        yield response


@pytest.fixture()
def fare_response():
    fare_path = DATA_DIR / "fare.json"
    with fare_path.open() as f:
        content = f.read()
        response = MagicMock(spec=Response, status_code=200, content=content)
        response.json.return_value = json.loads(content)
        yield response


@pytest.fixture()
def fare_list_response():
    fare_path = DATA_DIR / "fares.json"
    with fare_path.open() as f:
        content = f.read()
        response = MagicMock(spec=Response, status_code=200, content=content)
        response.json.return_value = json.loads(content)
        yield response


@pytest.fixture()
def siri_vm_archive_response():
    archive = DATA_DIR / "sirivm.zip"
    with archive.open("rb") as f:
        response = MagicMock(spec=Response, status_code=200, content=f.read())
        yield response


@pytest.fixture()
def gtfs_rt_archive_response():
    archive = DATA_DIR / "gtfsrt.zip"
    with archive.open("rb") as f:
        response = MagicMock(spec=Response, status_code=200, content=f.read())
        yield response
