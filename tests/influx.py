from enviro.destinations.influxdb import upload_reading, _prepare_payload
from enviro.helpers import uid, timestamp
from ucollections import OrderedDict

def test_upload_data():
    reading = {
            "nickname": "enviro",
            "timestamp": "2024-14-03T15:13:00Z",
            "readings": OrderedDict({
                "temperature": 30.05,
                "humidity": 50.40,
                "pressure": 989.00,
                "rain": 30
                }),
            "model": "weather",
            "uid": uid()
            }
    expected_result =f"weather_sensor,device=enviro temperature=30.05, humidity=50.40,pressure=989.00, rain=30 {timestamp(reading['timestamp'])}"
    
    try:
        assert _prepare_payload(reading) == expected_result
    except AssertionError as e:
        print(f"Test upload data failed: {_prepare_payload(reading)} is not equal to {expected_result}")

if __name__=="__main__":
    print('test')
    test_upload_data()
