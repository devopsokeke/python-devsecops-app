import pytest
import unittest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestApp(unittest.TestCase):
    def test_home(self):
        client = app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the DevSecOps Python App!", response.data)

    def test_health(self):
        client = app.test_client()
        response = client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"status":"healthy"', response.data)
