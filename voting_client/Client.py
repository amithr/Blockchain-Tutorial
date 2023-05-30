# This was mainly built for testing purposes to prototype the Wallet
# The real wallet is a Next.js application
# ECC cryptography library
from fastecdsa import keys, curve, ecdsa
import json, requests, hashlib

class Client:
    def __init__(self, node_address, private_key=None):
        self.node_address = node_address
        self.private_key = private_key or keys.gen_private_key(curve.P256)
        self.public_key = keys.get_public_key(self.private_key, curve.P256)
        self.public_hash = self.generate_public_hash()
    
    def generate_private_key_file(self):
        with open('private_key.txt', 'w') as f:
            f.write(self.private_key)
    
    # Is this necessary?
    def generate_public_hash(self):
        public_key_string = str(self.public_key.x) + str(self.public_key.y)
        encoded_json_public_key = public_key_string.encode()
        hash = hashlib.sha256(encoded_json_public_key).hexdigest()
        return hash

    def create_new_transaction(self, candidate):
        transaction_data = {
                'voter_public_key_x': self.public_key.x,
                'voter_public_key_y': self.public_key.y,
                'voter_hash': self.public_hash,
                'vote': candidate
        }
        
        # Convert dictionary to JSON to bytes for signing
        transaction = json.dumps(transaction_data)
        r, s = ecdsa.sign(transaction, self.private_key)
        signature = (r, s)

        transaction_request = {
            "data": transaction,
            "signature": signature
        }

        url = self.node_address + '/new-transaction-request'
        requests.post(url, json=transaction_request)

        # Returns both transaction and signature
        return transaction_request