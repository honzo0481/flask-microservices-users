"""User model tests."""

from project import db
from project.api.models import User
from project.api.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    """User model test suite."""

    def test_add_user(self):
        """You should be able to add a user to the db."""
        user = User(
            username='test@test.com',
            email='test@test.com'
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test@test.com')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)
