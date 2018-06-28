station_schema = """
{
  "namespace": "bikeshare_app",
  "type": "record",
  "name": "station_status",
  "fields": [
    {
      "name": "stationName", "type": ["null", "string"], "default": null
    },
    {
      "name": "availableDocks", "type": ["null", "int"], "default": null
    },
    {
      "name": "totalDocks", "type": ["null", "int"], "default": null
    },
    {
      "name": "latitude", "type": ["null", "double"], "default": null
    },
    {
      "name": "longitude", "type": ["null", "double"], "default": null
    },
    {
      "name": "statusValue", "type": ["null", "string"], "default": null
    },
    {
      "name": "statusKey", "type": ["null", "int"], "default": null
    },
    {
      "name": "availableBikes", "type": ["null", "int"], "default": null
    },
    {
      "name": "stAddress1", "type": ["null", "string"], "default": null
    },
    {
      "name": "stAddress2", "type": ["null", "string"], "default": null
    },
    {
      "name": "city", "type": ["null", "string"], "default": null
    },
    {
      "name": "postalCode", "type": ["null", "string"], "default": null
    },
    {
      "name": "location", "type": ["null", "string"], "default": null
    },
    {
      "name": "altitude", "type": ["null", "string"], "default": null
    },
    {
      "name": "testStation", "type": ["null", "boolean"], "default": null
    },
    {
      "name": "lastCommunicationTime", "type": ["null", "string"], "default": null
    },
    {
      "name": "landMark", "type": ["null", "string"], "default": null
    },
    {
      "name": "op", "type": ["null", "string"], "default": null
    }
  ]
}
"""
