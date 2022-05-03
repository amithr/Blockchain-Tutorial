import hashlib
from fastecdsa import curve, ecdsa, keys
import json, time

class Block:
    def __init__(self,  chain_index, proof_of_work_number, transaction, previous_hash, timestamp=None):
        self.chain_index = chain_index
        self.proof_of_work_number = proof_of_work_number
        self.transaction = transaction
        self.previous_hash = previous_hash
        if not timestamp:
            print("Timestamp generated.")
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp
    
    def calculate_hash(self):
        block_string = "{}{}{}{}{}".format(self.chain_index, 
            self.proof_of_work_number, self.transaction, self.previous_hash, self.timestamp).encode()
        hash = hashlib.sha256(block_string).hexdigest()
        return hash

    # Verify signature using transaction, signature tuple, and public key
    # Curve should match curve specified in the wallet
    @staticmethod
    def verify_transaction(signature, transaction, public_key):
        valid = ecdsa.verify(signature, transaction, public_key, curve=curve.P256)
        return valid
    
    def toJson(self):
        block_dict = {}
        block_dict["chain_index"] = self.chain_index
        block_dict["proof_of_work_number"] = self.proof_of_work_number
        block_dict["transaction"] = self.transaction
        block_dict["previous_hash"] = self.previous_hash
        block_dict["timestamp"] = self.timestamp

        return json.dumps(block_dict)
    
    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.chain_index, self.proof_of_work_number, self.transaction, self.previous_hash, self.timestamp)