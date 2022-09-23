from django.test import TestCase

# Create your tests here.

from django.test import TestCase
# Create your tests here.

import pytest
from django.test import Client


@pytest.fixture
def client():
    client = Client()
    return client


def test_login(client):
    response = client.get("/login/")
    assert response.status_code == 200