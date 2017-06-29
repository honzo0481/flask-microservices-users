"""Auth tests."""

import json

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    """Auth blueprint tests."""

    def test_user_registration(self):
        """A user should be able to register and get a success message back."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='test@test.com',
                    email='test@test.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'status')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        """Attempting to register a duplicate email should fail."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='rob',
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message']
            )
            self.assertIn('error', data['status'])

    def test_user_registration_duplicate_username(self):
        """Attempting to register a duplicate username should fail."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='test',
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message']
            )
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json(self):
        """Attempting to register with no data should fail."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        """Attempting to register without a username should fail."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        """Attempting to register without a username should fail."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        """Attempting to register without a username should fail."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='test@test.com',
                    email='test@test.com'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])
