from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Block import Block
from Blockchain import Blockchain
from blockchain_helpers import blockchain_validation
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def update_node_blockchain():
    update_url = app.state.node_address + '/update-blockchain'
    json_chain = jsonable_encoder(app.state.blockchain.chain)
    requests.post(update_url, json=json_chain)

@app.post("/new-transaction-request")
async def receive_new_transaction(transaction : Request):
    transaction = await transaction.json()
    new_block = app.state.blockchain.mine_block(transaction)
    json_new_block = new_block.toJson()
    app.state.blockchain.add_block_to_blockchain(new_block)
    if is_consensual(json_new_block):
        update_node_blockchain()

    return JSONResponse(content=json_new_block)


def is_consensual(json_new_block):
    consent_url = app.state.node_address + '/give-consent'
    response = requests.post(consent_url, json=json_new_block).json()
    if not response["valid"] == True:
        return False
    return True

# Immediately mine
# Send message to network when finished (all /give-consent routes)
# If consent received, add to local blockchain, otherwise remine
@app.post("/give-consent")
async def give_consent(new_block : Request):
    # The new block has been deserialized
    new_block = await new_block.json()
    print("give_consent Blockchain:", app.state.blockchain.chain.__repr__())
    new_block = Block(  
        new_block['chain_index'],
        new_block['proof_of_work_number'],
        new_block['transaction'],
        new_block['previous_hash'],
        new_block['timestamp']   
    )

    is_new_block_valid = blockchain_validation.is_new_block_valid(new_block, app.state.blockchain.get_last_block())
    if is_new_block_valid:
        app.state.blockchain.add_block_to_blockchain(new_block)
    print("Is Consent Given?", is_new_block_valid)
    # If valid, set last miner address
    json_message = jsonable_encoder({"valid":is_new_block_valid})
    return JSONResponse(content=json_message)


@app.post("/update-blockchain")
async def update_blockchain(blockchain : Request):
    # Need an easier way to serialize and deserialize blocks and blockchains
    blockchain = await blockchain.json()
    new_blockchain = convert_chain_list_to_blocks(blockchain)
    app.state.blockchain = Blockchain(new_blockchain)
    print("Secondary Node Update", app.state.blockchain.__repr__())
    json_message = jsonable_encoder({"updated":True})
    return JSONResponse(content=json_message)

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
    print("Secondary Node Timestamp", new_block.timestamp)
    return new_block