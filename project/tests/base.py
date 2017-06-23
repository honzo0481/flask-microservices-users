"""Base test module."""

from flask_testing import TestCase
from project import app, db


class BaseTestCase(TestCase):
    """A base test case for other test cases to inherit from."""

    def create_app(self):
        """Create an app and return it."""
        app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        """Create db objects and commit."""
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """End the session and drop db objects."""
        db.session.remove()
        db.drop_all()
