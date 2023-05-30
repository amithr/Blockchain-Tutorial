from blockchain_logic.Block import Block
from blockchain_logic.Blockchain import Blockchain

def convert_chain_list_to_blocks(chain):
    new_chain = []
    for dict_block in chain:
        block = convert_dict_to_block(dict_block)
        new_chain.append(block)
    return new_chain

def convert_dict_to_block(dict_block):
    new_block = Block(  
        dict_block['chain_index'],
        dict_block['proof_of_work_number'],
        dict_block['transaction'],
        dict_block['previous_hash'],
        dict_block['timestamp']     
    )
    return new_block


def convert_json_to_blockchain(api_request_blockchain):
    new_blockchain = convert_chain_list_to_blocks(api_request_blockchain)
    return Blockchain(new_blockchain)