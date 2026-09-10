from copy import deepcopy
import importlib

import pytest


app_module = importlib.import_module("src.app")


@pytest.fixture(autouse=True)
def isolate_activities(monkeypatch):
    monkeypatch.setattr(app_module, "activities", deepcopy(app_module.activities))