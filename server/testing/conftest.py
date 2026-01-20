#!/usr/bin/env python3

import pytest
from app import app
from models import db, User

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        if User.query.first() is None:
            # Create a test user if none exists
            test_user = User(username='testuser')
            db.session.add(test_user)
            db.session.commit()
        yield
        db.drop_all()