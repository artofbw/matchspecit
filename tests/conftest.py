import uuid
from typing import List
from unittest.mock import MagicMock

import pytest
from rest_framework.test import APIClient, APIRequestFactory

from matchspecit.project.models import Project
from matchspecit.technology.models import Technology


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_view():
    return MagicMock()


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def test_password():
    return "TestPassword"


@pytest.fixture
def create_technologies(db):
    def make_technology():
        Technology.objects.get_or_create(name="python")
        Technology.objects.get_or_create(name="java")
        Technology.objects.get_or_create(name="c++")
        return Technology.objects.all()

    return make_technology


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_project():
    def make_project(**kwargs):
        return Project.objects.create(name="test name", **kwargs)

    return make_project


@pytest.fixture
def create_technology():
    def make_technology():
        return Technology.objects.create(name=str(uuid.uuid4()))

    return make_technology
