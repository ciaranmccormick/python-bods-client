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
using the `get_gtfs_rt_data_feed` method with a boundng box.

```python

from bods_client.client import BODSClient
from bods_client.models import BoundingBox, GTFSRTParams

# An API key can be obtained by registering with the Bus Open Data Service
# https://data.bus-data.dft.gov.uk/account/signup/
>> API_KEY = "api-key"

>> bods = BODSClient(api_key=API_KEY)
>> box = BoundingBox(min_longitude=-0.54, min_latitude=51.26, max_longitude=0.27, max_latitide=51.75)
>> params = GTFSRTParams(bounding_box=box)
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
from bods_client.models import BoundingBox, SIRIVMParams
from lxml import etree

# An API key can be obtained by registering with the Bus Open Data Service
# https://data.bus-data.dft.gov.uk/account/signup/
>> API_KEY = "api-key"

>> bods = BODSClient(api_key=API_KEY)
>> box = BoundingBox(min_longitude=-0.54, min_latitude=51.26, max_longitude=0.27, 
  max_latitide=51.75)
>> params = SIRIVMParams(bounding_box=box)
>> siri = bods.get_siri_vm_data_feed(params=params)
>> siri
b'<Siri xmlns="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.siri.org.uk/siri http://www.siri.org.uk/schema/2.0/xsd/siri.xsd" version="2.0"><ServiceDelivery><ResponseTimestamp>2021-03-16T20:21:25.019277+00:00</ResponseTimestamp><ProducerRef>ItoWorld</ProducerRef><VehicleMonitoringDelivery><ResponseTimestamp>2021-03-16T20:21:25.019277+00:00</ResponseTimestamp><RequestMessageRef>d497da8c-1f05-4db0-8680-dadfb22939b5</RequestMessageRef><ValidUntil>2021-03-16T20:26:25.019277+00:00</ValidUntil>
...
<DriverRef>111133</DriverRef></VehicleJourney></Extensions></VehicleActivity></VehicleMonitoringDelivery></ServiceDelivery></Siri>'
>> xml = etree.parse(siri)
```

Details about the SIRI specification can be found [here](http://www.transmodel-cen.eu/standards/siri/).


## License

[MIT](https://github.com/ciaran.mccormick/bods-client/blob/master/LICENSE)


