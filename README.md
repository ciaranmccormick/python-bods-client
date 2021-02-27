# bods-client

[![Build Status](https://github.com/ciaranmccormick/python-bods-client/workflows/test/badge.svg?branch=master&event=push)](https://github.com/ciaranmccormick/python-bods-client/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/ciaranmccormick/python-bods-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ciaranmccormick/python-bods-client)
[![Python Version](https://img.shields.io/pypi/pyversions/bods-client.svg)](https://pypi.org/project/bods-client/)

A Python client for the Department for Transport Bus Open Data Service API


## Installation

```bash
pip install bods-client
```


## Example


### GTFS RT

All the vehicle locations for vehicles in a geographical location can be obtained
using the `get_gtfs_rt_data_feed` method with a boundng box.

```python

from bods_client.client import BODSClient
from bods_client.models import BoundingBox

# An API key can be obtained by registering with the Bus Open Data Service
# https://data.bus-data.dft.gov.uk/account/signup/
>> API_KEY = "api-key"

>> bods = BODSClient(api_key=API_KEY)
>> box = BoundingBox(min_longitude=-0.54, min_latitude=51.26, max_longitude=0.27, max_latitide=51.75)
>> message = bods.get_gtfs_rt_data_feed(bounding_box=box)
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


## License

[MIT](https://github.com/ciaran.mccormick/bods-client/blob/master/LICENSE)


