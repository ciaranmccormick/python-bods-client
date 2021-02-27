BODS_API_URL = "https://data.bus-data.dft.gov.uk/api"

V1 = BODS_API_URL + "/v1"

V1_TIMETABLES_URL = V1 + "/dataset"
V1_FARES_URL = V1 + "/fares/dataset"
V1_GTFS_RT_URL = V1 + "/gtfsrtdatafeed"
V1_SIRI_VM_URL = V1 + "/datafeed"

DATASET_STATUSES = ["published", "error", "expired", "inactive"]
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

OK_200 = 200
NOT_FOUND_404 = 404
