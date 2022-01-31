from datetime import datetime
from pathlib import Path

import pytest

from bods_client.models import Siri
from bods_client.models.siri import SiriParsingError, VehicleActivity

DATA = Path(__file__).parent / "data"


def test_siri_from_bytes():
    good = DATA / "good_packet.xml"
    with good.open("rb") as f:
        siri = Siri.from_bytes(f.read())

    activities = siri.service_delivery.vehicle_monitoring_delivery.vehicle_activities
    assert len(activities) == 4
    vehicle_activity: VehicleActivity = activities[0]
    assert vehicle_activity.recorded_at_time == datetime.fromisoformat(
        "2022-01-29T16:09:19+00:00"
    )
    assert vehicle_activity.item_identifier == "8fa128ab-ef16-428a-81c0-5fec77bc4f66"
    assert vehicle_activity.valid_until_time == datetime.fromisoformat(
        "2022-01-29T19:54:42.330948"
    )
    mvj = vehicle_activity.monitored_vehicle_journey
    assert mvj.published_line_name == "9"
    assert mvj.operator_ref == "AKSS"
    assert mvj.destination_ref == "2400A001770A"
    assert mvj.vehicle_location is not None
    assert mvj.vehicle_location.longitude == 0.557191
    assert mvj.vehicle_location.latitude == 51.277118
    assert mvj.block_ref == "0320"
    assert mvj.vehicle_ref == "6409"


def test_missing_service_delivery():
    missing = DATA / "missing_service_delivery.xml"
    with missing.open("rb") as f:
        with pytest.raises(SiriParsingError):
            Siri.from_bytes(f.read())


def test_missing_vehicle_monitoring_delivery():
    missing = DATA / "missing_vmd.xml"
    with missing.open("rb") as f:
        with pytest.raises(SiriParsingError):
            Siri.from_bytes(f.read())


def test_missing_monitored_vehicle_journey():
    missing = DATA / "missing_mvj.xml"
    with missing.open("rb") as f:
        with pytest.raises(SiriParsingError):
            Siri.from_bytes(f.read())


def test_missing_vehicle_location():
    missing = DATA / "missing_vehicle_location.xml"
    with missing.open("rb") as f:
        with pytest.raises(SiriParsingError):
            Siri.from_bytes(f.read())


def test_missing_vehicle_journey_refs():
    missing = DATA / "missing_vj_ref.xml"
    with missing.open("rb") as f:
        siri = Siri.from_bytes(f.read())

    assert isinstance(siri, Siri)
    vehicles = siri.service_delivery.vehicle_monitoring_delivery.vehicle_activities
    mvj = vehicles[0].monitored_vehicle_journey
    assert mvj.framed_vehicle_journey_ref is None
    assert mvj.vehicle_journey_ref is None
