from fastecdsa import curve, ecdsa
from fastecdsa.point import Point
import json, hashlib


def is_vote_valid(chain, transaction):
    transaction_data = json.loads(transaction["data"])
    voter_hash = transaction_data["voter_hash"]
    # Check that this person didn't vote anywhere else in the blockchain
    single_vote = True
    # First block will be the genesis block, anyways
    if len(chain) > 2:
        for index in range(1, len(chain)):
            block = chain[index]
            if block.transaction and block.transaction["voter_hash"] == voter_hash:
                single_vote = False
    
    return single_vote

def is_transaction_crypto_valid(transaction):
    # Make sure transaction is valid by cryptographically comparing transaction signature
    # and sender's public key
    # Convert the public key coordinates back into a Point object that holds both, in order to use
    # the verify function
    transaction_data = json.loads(transaction["data"])
    voter_public_key = Point(transaction_data["voter_public_key_x"], transaction_data["voter_public_key_y"], curve=curve.P256)
    # Check that the transaction itself is valid (in JSON form)
    # Check for signature validity
    is_signature_valid = ecdsa.verify(transaction["signature"], 
        transaction["data"], # Need to verify original transaction, which is json format
        voter_public_key, curve=curve.P256)

    voter_hash = transaction_data["voter_hash"]
    public_key_string = str(transaction_data["voter_public_key_x"]) + str(transaction_data["voter_public_key_y"])
    hashed_public_key = hashlib.sha256(public_key_string.encode()).hexdigest()

    if hashed_public_key != voter_hash:
        return False
    if not is_signature_valid:
        return False
    return True


# Check if hash can be generated using public key supplied
# Compare signature to public key
# Make sure that the hash doesn't exist anywhere else in the blockchain

def is_transaction_valid(chain, transaction):
    if not is_vote_valid(chain, transaction):
        return False
    if not is_transaction_crypto_valid(transaction): 
        return False
    return True