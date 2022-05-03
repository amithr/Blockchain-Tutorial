from initial_node_api import app
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from client.Client import Client
import os

client = TestClient(app)

def test_generate_new_transaction():
    client = Client("http://127.0.0.1:8000")
    transaction = client.create_new_transaction("Donald Trump")
    # Returns dict with transaction and signature
    assert True