"""Configuration tests module."""

import unittest

from flask import current_app
from flask_testing import TestCase

from project import app


class TestDevelopmentConfig(TestCase):
    """Development config tests."""

    def create_app(self):
        """Create an app and return it."""
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """Config settings should be a match for dev."""
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgres://postgres:postgres@users-db:5432/users_dev'
        )


class TestTestingConfig(TestCase):
    """Test config tests."""

    def create_app(self):
        """Create an app and return it."""
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """Config settings should be a match for test."""
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgres://postgres:postgres@users-db:5432/users_test'
        )


class TestProductionConfig(TestCase):
    """Production config tests."""

    def create_app(self):
        """Create an app and return it."""
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """Config settings should be a match for dev."""
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
