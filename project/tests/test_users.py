"""User tests module."""

import json
import datetime
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the user service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='rob',
                    email='gonzalesre@gmail.com',
                    password='test'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('gonzalesre@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """An error should be thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """An error should be thrown if the JSON object does not have a username key."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='gonzalesre@gmail.com')),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """An error should be thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='rob',
                    email='gonzalesre@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='rob',
                    email='gonzalesre@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message']
            )
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Getting a single user should return exactly that users's data."""
        user = add_user('rob', 'gonzalesre@gmail.com', 'test')
        with self.client:
            response = self.client.get(f'/users/{user.id}') # noqa
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('rob', data['data']['username'])
            self.assertIn('gonzalesre@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """An error should be thrown if no id is provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_incorrect_id(self):
        """An error should be thrown if the provided id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Getting all users should return all user's data."""
        created = datetime.datetime.now() + datetime.timedelta(-30)
        add_user('rob', 'gonzalesre@gmail.com', 'test', created)
        add_user('bob', 'test@test.com', 'test')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('bob', data['data']['users'][0]['username'])
            self.assertIn(
                'test@test.com', data['data']['users'][0]['email']
            )
            self.assertIn('rob', data['data']['users'][1]['username'])
            self.assertIn('gonzalesre@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """An error should be thrown if the JSON object does not have a password key."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='rob',
                    email='gonzalesre@gmail.com')),
                    content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
