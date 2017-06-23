"""User tests module."""

import json
from project.tests.base import BaseTestCase


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
        """Adding a new user to the db should be possible."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    useruser='robert',
                    email='gonzalesre@gmail.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('gonzalesre@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])
