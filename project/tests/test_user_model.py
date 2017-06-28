"""User model tests."""

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    """User model test suite."""

    def test_add_user(self):
        """You should be able to add a user to the db."""
        user = add_user('test@test.com', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test@test.com')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_user_duplicate_username(self):
        """Adding a duplicate username should fail."""
        add_user('test@test.com', 'test@test.com', 'test')
        duplicate_user = User(
            username='test@test.com',
            email='test@test2.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        """Adding a duplicate email should fail."""
        add_user('test@test.com', 'test@test.com', 'test')
        duplicate_user = User(
            username='test@test2.com',
            email='test@test.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        """All Passwords should be random."""
        user_one = add_user('test@test.com', 'test@test.com', 'test')
        user_two = add_user('test@test2.com', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        """User model should be able to generate encoded auth tokens."""
        user = add_user('test@test.com', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """User model should return user_id when decoded."""
        user = add_user('test@test.com', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token), user.id)
