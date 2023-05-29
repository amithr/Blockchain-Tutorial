from warnings import catch_warnings
from .Block import Block
import json
from blockchain_logic.blockchain_helpers import proof_of_work, blockchain_validation, transaction_validation

class Blockchain:
    def __init__(self, chain=[]):
        self.chain = chain
        # If new blockchain, construct first block on chain
        if len(self.chain) == 0:
            print('hello')
            self.construct_genesis()

    def construct_genesis(self):
        genesis_block = Block(chain_index=0, proof_of_work_number=0, transaction="{}", previous_hash='0')
        self.chain.append(genesis_block)
    
    def get_last_block(self):
        return self.chain[-1]
    
    def update_blockchain(self, new_blockchain):
        self.chain = new_blockchain
    
    def create_new_block(self, proof_number, previous_hash, transaction):
        is_transaction_valid = transaction_validation.is_transaction_valid(self.chain, transaction)

        # If transaction is valid, generate new block
        new_block = None
        if is_transaction_valid:
            new_block = Block(
                chain_index = len(self.chain),
                proof_of_work_number = proof_number,
                # Turn into a dict from json
                transaction = json.loads(transaction["data"]),
                previous_hash = previous_hash
            )
        else:
            raise Exception("Transaction invalid.")
        
        return new_block
    

    # Do mining
    def mine_block(self, transaction):
        proof_of_work_number = proof_of_work.generate_next_proof_of_work_number(self.get_last_block())
        previous_hash = self.get_last_block().calculate_hash()
        return self.create_new_block(proof_of_work_number, previous_hash, transaction)
    
    def add_block_to_blockchain(self, new_block):
        last_block = self.get_last_block()
        is_block_valid = blockchain_validation.is_new_block_valid(new_block, last_block)
        
        if is_block_valid:
            self.chain.append(new_block)
        else:
            raise Exception("Block invalid.")

        return self.chain

    def __repr__(self):
        display_block_list = []
        for block in self.chain:
            display_block_list.append(block.__repr__())
        return display_block_list
