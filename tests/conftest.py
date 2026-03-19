import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

# Capture the original seed data once at import time
_SEED_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore in-memory activities to seed state before every test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_SEED_ACTIVITIES))
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
