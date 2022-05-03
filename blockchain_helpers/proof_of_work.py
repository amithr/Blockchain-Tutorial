import hashlib
# Identifies a new proof_no such that the hash of the new proof_no multiplied by the current
# proof_no has 4 leading zeroes (0000). This is the mining operation.
def generate_next_proof_of_work_number(last_block):
    new_proof_of_work_number = 0
    # Keep incrementing proof number until we obtain a new hash with 4 leading zeroes
    # This is the the computationally intensive task that makes mining expensive
    while not try_next_proof_of_work_number(new_proof_of_work_number, last_block.proof_of_work_number):
        new_proof_of_work_number += 1

    return new_proof_of_work_number

# Used both to generate the next proof of work number and to verify
# proposed blocks from other nodes
def try_next_proof_of_work_number(new_proof_number, last_proof_number):
    # Generate a UTF string with both proof numbers
    new_proof_number_guess = f'{new_proof_number}{new_proof_number}'.encode()
    # Hash this
    guess_hash = hashlib.sha256(new_proof_number_guess).hexdigest()
    return guess_hash[:4] == "0000"