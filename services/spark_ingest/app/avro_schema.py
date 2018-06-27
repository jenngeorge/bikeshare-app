station_schema = """
{
  "namespace": "bikeshare_app",
  "type": "record",
  "name": "station_status",
  "fields": [
    {
      "name": "stationName", "type": "string"
    },
    {
      "name": "availableDocks", "type": "int"
    },
    {
      "name": "totalDocks", "type": "int"
    },
    {
      "name": "latitude", "type": "double"
    },
    {
      "name": "longitude", "type": "double"
    },
    {
      "name": "statusValue", "type": "string"
    },
    {
      "name": "statusKey", "type": "int"
    },
    {
      "name": "availableBikes", "type": "int"
    },
    {
      "name": "stAddress1", "type": "string"
    },
    {
      "name": "stAddress2", "type": "string"
    },
    {
      "name": "city", "type": "string"
    },
    {
      "name": "postalCode", "type": "string"
    },
    {
      "name": "location", "type": "string"
    },
    {
      "name": "altitude", "type": "string"
    },
    {
      "name": "testStation", "type": "boolean"
    },
    {
      "name": "lastCommunicationTime", "type": "string"
    },
    {
      "name": "landMark", "type": "string"
    },
    {
      "name": "op", "type": "string"
    }
  ]
}
"""
