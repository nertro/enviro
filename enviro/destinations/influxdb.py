from enviro import logging
from enviro.constants import UPLOAD_SUCCESS, UPLOAD_FAILED
from enviro.helpers import timestamp as create_timestamp
import urequests, time
import config

def url_encode(t):
  result = ""
  for c in t:
    # no encoding needed for character
    if c.isalpha() or c.isdigit() or c in ["-", "_", "."]:
      result += c
    elif c == " ":
      result += "+"
    else:
      result += f"%{ord(c):02X}"
  return result

def log_destination():
  logging.info(f"> uploading cached readings to Influxdb bucket: {config.influxdb_bucket}")

def _prepare_payload(reading):
  sensor_readings = []
  for sensor, fields in reading['readings'].items():
    measurements = ",".join([f"{field}={val}"
                           for field,val in fields.items()
                             ])
    sensor_readings.append(f"{sensor},device={reading['nickname']},station=enviro_{reading['model']} {measurements} {create_timestamp(reading['timestamp'])}")
  return "\n".join(sensor_readings)

def _prepare_legacy_payload(reading):
  payload = ""
  timestamp = create_timestamp(reading['timestamp'])
  nickname = reading["nickname"]
  if isinstance(list(reading["readings"].values())[0], dict):
    readings = {}
    for sensor, sensor_readings in reading['readings'].items():
      readings.update(sensor_readings)
    reading["readings"] = readings

  return "\n".join(
    f"{key},device={nickname} value={value} {timestamp}"
    for key, value in reading['readings'].items()
   )
  return payload

def upload_reading(reading, legacy=True):  
  headers = {
    "Authorization": f"Token {config.influxdb_token}"
    }
  
  if legacy:
      payload = _prepare_legacy_payload(reading)
  else:
      payload = _prepare_payload(reading)

  bucket = url_encode(config.influxdb_bucket)
  org = url_encode(config.influxdb_org)
  url = "/".join([
    config.influxdb_url,
    "api/v2",
    f"write?precision=s&org={org}&bucket={bucket}"
  ])
 
  try:
    # post reading data to http endpoint
    result = urequests.post(url, headers=headers, data=payload)
    result.close()
    
    if result.status_code == 204:  # why 204? we'll never know...
      return UPLOAD_SUCCESS

    logging.debug(f"  - upload issue ({result.status_code} {result.reason})")
  except Exception as e:
    logging.debug(f" - an exception occurred when uploading: {e}")

  return UPLOAD_FAILED
