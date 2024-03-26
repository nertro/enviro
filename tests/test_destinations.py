from enviro.destinations.influxdb import upload_reading, _prepare_payload
from enviro.helpers import uid, timestamp
from ucollections import OrderedDict
import unittest


class TestInflux(unittest.TestCase):

    def test_payload_creation(self):
        reading = {
            "nickname":
            "enviro",
            "timestamp":
            "2024-14-03T15:13:00Z",
            "readings":
            OrderedDict({
                "temperature": 30.05,
                "humidity": 50.42,
                "pressure": 989.01,
                "rain": 30
            }),
            "model":
            "weather",
            "uid":
            uid()
        }
        expected_result = f"weather_sensor, device=enviro temperature=30.05, humidity=50.42, pressure=989.01, rain=30 {timestamp(reading['timestamp'])}"

        self.assertEqual(_prepare_payload(reading), expected_result)


if __name__ == "__main__":
    print("Testing destinations.")
    print(sys.path)
    print(os.listdir('.'))
    unittest.main()
