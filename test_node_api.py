from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from voting_client.Client import Client
import os

def test_generate_new_transaction():
    client = Client("http://127.0.0.1:5001")
    transaction = client.create_new_transaction("Hilary Clinton")
    # Returns dict with transaction and signature
    assert True