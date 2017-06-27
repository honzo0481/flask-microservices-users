"""Testing utilities."""

import datetime

from project import db
from project.api.models import User


def add_user(username, email, password, create_at=datetime.datetime.now()):
    """Add a user to the database."""
    user = User(
        username=username,
        email=email,
        password=password,
        created_at=create_at
    )
    db.session.add(user)
    db.session.commit()
    return user
