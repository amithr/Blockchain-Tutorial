from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from blockchain_logic.Block import Block
from blockchain_logic.Blockchain import Blockchain
from blockchain_logic.blockchain_helpers import blockchain_validation
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

origins = ["*"]

app.state.node_list = set() # This is actually a set - ensures that only unique values are added
app.state.blockchain = None
app.state.command_node = "http://127.0.0.1:8000"


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_json_to_blockchain(api_request_blockchain):
    new_blockchain = convert_chain_list_to_blocks(api_request_blockchain)
    return Blockchain(new_blockchain)

@app.on_event("startup")
def startup_event():
    # Reach out to the command node
    # Get node list
    # Get current block chain
    command_node_blockchain_url = app.state.command_node + "/initialize-node-blockchain"
    most_recent_blockchain = requests.post(command_node_blockchain_url).json()
    app.state.blockchain = convert_json_to_blockchain(most_recent_blockchain)
    command_node_node_list_url = app.state.command_node + "/initialize-node-list"
    most_recent_node_list = requests.post(command_node_node_list_url)
    if most_recent_node_list:
        app.state.node_list = most_recent_node_list.json()
    print("Child Node Latest Blockchain", app.state.blockchain.__repr__())
    print("Node List", app.state.node_list)
    print("Node online")

def is_consensual(json_new_block):
    for node_address in app.state.node_list:
        consent_url = node_address + '/give-consent'
        try:
            response = requests.post(consent_url, json=json_new_block).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("Couldn't contact peer node for consent", node_address)
            continue
        except requests.exceptions.HTTPError:
            print("4xx, 5xx")
            continue
        else:
            print("Peer node successfully contacted", node_address)
            if not response["valid"] == True:
                return False
            print("Consent from ", node_address)
    return True
    

@app.post("/new-transaction-request")
async def receive_new_transaction(transaction : Request):
    transaction = await transaction.json()
    new_block = app.state.blockchain.mine_block(transaction)
    json_new_block = jsonable_encoder(new_block)
    print("New Transaction Request Block", json_new_block)
    if is_consensual(json_new_block):
        print("Is Consensual (Primary Node)")
        app.state.blockchain.add_block_to_blockchain(new_block)
        # Update command blockchain
        command_node_blockchain_url = app.state.command_node + "/update-command-blockchain"

    return JSONResponse(content=json_new_block)

@app.post("/update-node-list")
async def update_node_list(node_list : Request):
    node_list = await node_list.json()
    for node_address in node_list:
        app.state.node_list.add(node_address)
    print("Nodes updated")

# Immediately mine
# Send message to network when finished (all /give-consent routes)
# If consent received, add to local blockchain, otherwise remine
@app.post("/give-consent")
async def give_consent(new_block : Request):
    # The new block has been deserialized
    new_block = await new_block.json()
    new_block = Block(  
        new_block['chain_index'],
        new_block['proof_of_work_number'],
        new_block['transaction'],
        new_block['previous_hash'],
        new_block['timestamp']   
    )
    print("New Block", new_block)
    print("Blockchain", app.state.blockchain.__repr__())
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
    app.state.blockchain = convert_json_to_blockchain(blockchain)
    print("Node Update", app.state.blockchain.__repr__())
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
    print("Child Node Timestamp", new_block.timestamp)
    return new_block