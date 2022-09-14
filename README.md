# bods-client

[![Build Status](https://github.com/ciaranmccormick/python-bods-client/workflows/test/badge.svg?branch=main&event=push)](https://github.com/ciaranmccormick/python-bods-client/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/ciaranmccormick/python-bods-client/branch/main/graph/badge.svg)](https://codecov.io/gh/ciaranmccormick/python-bods-client)
[![Python Version](https://img.shields.io/pypi/pyversions/bods-client.svg)](https://pypi.org/project/bods-client/)

A Python client for the Department for Transport Bus Open Data Service API


## Installation

```bash
pip install bods-client
```


## Example


### GTFS RT

All the vehicle locations for vehicles in a geographical location can be obtained
using the `get_gtfs_rt_data_feed` method with a bounding box.

```python

from bods_client.client import BODSClient
from bods_client.models import BoundingBox, GTFSRTParams

# An API key can be obtained by registering with the Bus Open Data Service
# https://data.bus-data.dft.gov.uk/account/signup/
>> API_KEY = "api-key"

>> bods = BODSClient(api_key=API_KEY)
>> bounding_box = BoundingBox(
    **{
        "min_latitude": 51.26,
        "max_latitude": 51.75,
        "min_longitude": -0.54,
        "max_longitude": 0.27,
    }
)
>> params = GTFSRTParams(bounding_box=bounding_box)
>> message = bods.get_gtfs_rt_data_feed(params=params)
>> message.entity[0]
id: "421354378097713049"
vehicle {
  trip {
    trip_id: ""
    route_id: ""
  }
  position {
    latitude: 51.712860107421875
    longitude: -0.38401100039482117
    bearing: 170.0
  }
  timestamp: 1614396229
  vehicle {
    id: "7214"
  }
}

```

This returns a `google.transit.gtfs_realtime_pb2.FeedMessage` object. More details about
General Transit Feed Specification Realtime Transit (GTFS-RT) can be found
[here](https://developers.google.com/transit/gtfs-realtime/).


### SIRI VM

Vehicle locations are also provided in the SIRI-VM XML format using the
`get_siri_vm_data_feed` method. The data can then parsed using an xml
parser library such as `lxml`.

```python
from bods_client.client import BODSClient
from bods_client.models import BoundingBox, Siri, SIRIVMParams


>> API_KEY = "api-key"

>> client = BODSClient(api_key=API_KEY)
>> bounding_box = BoundingBox(
    **{
        "min_latitude": 51.267729,
        "max_latitude": 51.283191,
        "min_longitude": -0.142423,
        "max_longitude": 0.177432,
    }
)

>> params = SIRIVMParams(bounding_box=bounding_box)
>> siri_response = client.get_siri_vm_data_feed(params=params)
>> siri = Siri.from_bytes(siri_response)
>> siri.service_delivery.vehicle_monitoring_delivery.vehicle_activities[0]
VehicleActivity(
    recorded_at_time=datetime.datetime(
        2022, 1, 31, 19, 48, 24, tzinfo=datetime.timezone.utc
    ),
    item_identifier="05fc46f3-9629-4336-9a8d-f397030f5891",
    valid_until_time=datetime.datetime(2022, 1, 31, 21, 5, 21, 997139),
    monitored_vehicle_journey=MonitoredVehicleJourney(
        bearing=135.0,
        block_ref=None,
        framed_vehicle_journey_ref=None,
        vehicle_journey_ref="447183",
        destination_name="BEDDINGTON (ABELLIO LONDON)",
        destination_ref=None,
        orgin_name=None,
        origin_ref="40004410084D",
        origin_aimed_departure_time=datetime.datetime(
            2022, 1, 31, 19, 53, tzinfo=datetime.timezone.utc
        ),
        direction_ref="1",
        published_line_name="407",
        line_ref="296",
        vehicle_location=VehicleLocation(longitude=-0.077464, latitude=51.282658),
        operator_ref="TFLO",
        vehicle_ref="16085",
    ),
)
```

Details about the SIRI specification can be found [here](http://www.transmodel-cen.eu/standards/siri/).


## License

[MIT](https://github.com/ciaran.mccormick/bods-client/blob/master/LICENSE)
