
from .proof_of_work import try_next_proof_of_work_number

def is_new_block_valid(new_block, last_block):
    if last_block.chain_index ==  new_block.chain_index:
        print("The chain index hasn't been incremented.")
        return False
    if new_block.timestamp <= last_block.timestamp:
        print("Timestamp of new block is not bigger than last block.")
        return False
    if not try_next_proof_of_work_number(new_block.proof_of_work_number, last_block.proof_of_work_number):
        print(3)
        print("Proof of work isn't valid.")
        return False
    if last_block.calculate_hash() != new_block.previous_hash:
        print(last_block.calculate_hash())
        print(new_block.previous_hash)
        print("Hashes don't match.")
        return False
    # Make sure voter was not on the blockchain anywhere else
    print("The block is valid and consistent with the rest of the blockchain.")
    return True