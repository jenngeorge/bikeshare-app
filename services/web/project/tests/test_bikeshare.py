
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
                    'status_key': 1,
                    'land_mark': None,
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
                    'status_key': 1,
                    'land_mark': None,
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
        """Ensure error is thrown if the station already exists."""
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
                    'status_key': 1,
                    'land_mark': None,
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

    # Update station tests
    def test_update_station(self):
        """Ensure a station can be updated in the database."""
        with self.client:
            self.client.post(
                '/stations',
                data=json.dumps({
                    'id': 26,
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            response = self.client.put(
                '/stations/26',
                data=json.dumps({'station_name': 'New station name!'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('station 26 was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_station_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty when updating."""
        response = self.client.put(
            '/stations/26',
            data=json.dumps({}),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_update_station_invalid_id(self):
        """
        Ensure error is thrown if the JSON object has an invalid id when updating.
        """
        with self.client:
            response = self.client.put(
                '/stations/32',
                data=json.dumps({
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            self.assertEqual(response.status_code, 404)
            self.assertIn('Station id does not exist', data['message'])
            self.assertIn('fail', data['status'])

    # get a station
    def test_single_station(self):
        """Ensure get single station behaves correctly"""
        with self.client:
            self.client.post(
                '/stations',
                data=json.dumps({
                    'id': 26,
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            response = self.client.get('/stations/26')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Best Station', data['data']['station_name'])
            self.assertIn('success', data['status'])

    def test_single_station_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = self.client.get('stations/recurse')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Station does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_station_incorrect_id(self):
        """Ensure error is thrown if the id does not exist"""
        with self.client:
            response = self.client.get('stations/1001')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Station does not exist', data['message'])
            self.assertIn('fail', data['status'])

    # Delete station tests
    def test_delete_station(self):
        """Ensure a station can be deleted in the database."""
        with self.client:
            self.client.post(
                '/stations',
                data=json.dumps({
                    'id': 26,
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            response = self.client.delete(
                '/stations/26'
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('station 26 was deleted!', data['message'])
            self.assertIn('success', data['status'])

    def test_delete_station_and_histories(self):
        """Ensure a station can be deleted in the database."""
        with self.client:
            self.client.post(
                '/stations',
                data=json.dumps({
                    'id': 26,
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            # add station history
            self.client.post(
                '/station_histories',
                data=json.dumps({
                    'station_id': 26,
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            response = self.client.delete(
                '/stations/26'
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('station 26 was deleted!', data['message'])
            self.assertIn('success', data['status'])

    def test_delete_station_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = self.client.get('stations/recurse')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Station does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_delete_station_incorrect_id(self):
        """Ensure error is thrown if the id does not exist"""
        with self.client:
            response = self.client.get('stations/1001')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Station does not exist', data['message'])
            self.assertIn('fail', data['status'])

    # station history tests
    def test_add_station_history(self):
        """Ensure a new station history can be added to the database."""
        with self.client:
            # make a station
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
                    'status_key': 1,
                    'land_mark': None,
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
            # test adding history for that station
            response = self.client.post(
                '/station_histories',
                data=json.dumps({
                    'station_id': 24,
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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
            print(data['message'])
            self.assertEqual(response.status_code, 201)
            self.assertIn('station 24 new history was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_station_history_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/station_histories',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_station_history_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a station id key.
        """
        with self.client:
            response = self.client.post(
                '/station_histories',
                data=json.dumps({
                    'station_name': 'Best Station',
                    'available_docks': 10,
                    'total_docks': 35,
                    'latitude': 40.741895,
                    'longitude': -73.989308,
                    'status_value': 'In Service',
                    'status_key': 1,
                    'land_mark': None,
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


if __name__ == '__main__':
    unittest.main()
