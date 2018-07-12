
import json
import unittest

from project.tests.base import BaseTestCase


class TestBikeshareAPIService(BaseTestCase):
    """Tests for the Bikeshare API Service."""

    def test_bikeshare(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/bikeshare/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_station(self):
        """Ensure a new station can be added to the database."""
        with self.client:
            response = self.client.post(
                '/stations',
                data=json.dumps({
                    'id': '24',
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_value': 1,
                    'available_bikes': 24,
                    'st_address_1': '995 Pacific St',
                    'st_address_2': None,
                    'city': None,
                    'postal_code': '11215',
                    'location': None,
                    'altitude': None,
                    'test_station': False,
                    'last_communication_time': '2018-07-12 06:51:58 PM'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('station 24 was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_station_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/stations',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_station_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have an id key.
        """
        with self.client:
            response = self.client.post(
                '/stations',
                data=json.dumps({
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_value': 1,
                    'available_bikes': 24,
                    'st_address_1': '995 Pacific St',
                    'st_address_2': None,
                    'city': None,
                    'postal_code': '11215',
                    'location': None,
                    'altitude': None,
                    'test_station': False,
                    'last_communication_time': '2018-07-12 06:51:58 PM'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload: Must include a station id', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_station_duplicate_id(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/stations',
                data=json.dumps({
                    'id': '24',
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_value': 1,
                    'available_bikes': 24,
                    'st_address_1': '995 Pacific St',
                    'st_address_2': None,
                    'city': None,
                    'postal_code': '11215',
                    'location': None,
                    'altitude': None,
                    'test_station': False,
                    'last_communication_time': '2018-07-12 06:51:58 PM'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/stations',
                data=json.dumps({'id': '24', 'station_name': 'same station!'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That station id already exists.', data['message'])
            self.assertIn('fail', data['status'])

if __name__ == '__main__':
    unittest.main()
