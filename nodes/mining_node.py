from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from blockchain_logic.Block import Block
from blockchain_logic.blockchain_helpers import blockchain_validation
from fastapi.middleware.cors import CORSMiddleware
from node_helper import convert_json_to_blockchain
from logger.Logger import Logger
from logger import log_constants
import requests

# https://github.com/permitio/fastapi_websocket_pubsub

app = FastAPI()

origins = ["*"]

app.state.node_list = set() # This is actually a set - ensures that only unique values are added
app.state.blockchain = None
app.state.command_node = ""
app.state.port = 0
app.state.id=0
app.state.user_id=""
app.state.address=""
app.state.logger = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/initialize-mining-node")
async def initialize_mining_node(data: Request):
    data = await data.json()
    app.state.command_node = data['command_node_address']
    app.state.port = data['port']
    app.state.id  = data['node_id']
    app.state.user_id = data['user_id']
    get_latest_blockchain(app.state.command_node)
    get_latest_node_list(app.state.command_node)
    app.state.logger = Logger(app.state.user_id, app.state.port, app.state.id)
    app.state.logger.emit_log('Mining node online and initialized.', log_constants.SUCCESS)
    return

def is_consensual(json_new_block):
    print(app.state.node_list)
    for node_address in app.state.node_list:
        consent_url = node_address + '/give-consent'
        try:
            response = requests.post(consent_url, json=json_new_block).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            app.state.logger.emit_log("Couldn't contact peer node for consent " + node_address, log_constants.ERROR)
            continue
        except requests.exceptions.HTTPError:
            print("4xx, 5xx")
            continue
        else:
            app.state.logger.emit_log("Peer node successfully contacted at " + node_address, log_constants.SUCCESS)
            if not response["valid"] == True:
                return False
            app.state.logger.emit_log("Consent from "+node_address+" achieved.", log_constants.SUCCESS)
    return True
    

@app.post("/new-transaction-request")
async def receive_new_transaction(transaction : Request):
    app.state.logger.emit_log("New transaction request received.", log_constants.RECEIVED)
    transaction = await transaction.json()
    get_latest_blockchain(app.state.command_node)
    get_latest_node_list(app.state.command_node)
    new_block = app.state.blockchain.mine_block(transaction)
    json_new_block = jsonable_encoder(new_block)
    if is_consensual(json_new_block):
        app.state.logger.emit_log("Consent achieved for new block.", log_constants.SUCCESS)
        app.state.blockchain.add_block_to_blockchain(new_block)
        # Update command blockchain with new, approved blockchain
        update_command_blockchain(app.state.command_node)

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
        app.state.logger.emit_log("Consent given for new block.", log_constants.SUCCESS)
    else:
        app.state.logger.emit_log("Consent not given for new block.", log_constants.ERROR)
    # If valid, set last miner address
    json_message = jsonable_encoder({"valid":is_new_block_valid})
    return JSONResponse(content=json_message)

@app.post("/update-blockchain")
async def update_blockchain(blockchain : Request):
    # Need an easier way to serialize and deserialize blocks and blockchains
    blockchain = await blockchain.json()
    app.state.blockchain = convert_json_to_blockchain(blockchain)
    app.state.logger.emit_log("Node updated with latest blockchain.", log_constants.UPDATE)
    json_message = jsonable_encoder({"updated":True})
    return JSONResponse(content=json_message)

def get_latest_blockchain(command_node_address):
    command_node_blockchain_url = command_node_address + "/initialize-node-blockchain"
    most_recent_blockchain = requests.post(command_node_blockchain_url).json()
    app.state.blockchain = convert_json_to_blockchain(most_recent_blockchain)

def get_latest_node_list(command_node_address):
    command_node_node_list_url = command_node_address + "/initialize-node-list"
    most_recent_node_list = requests.post(command_node_node_list_url)
    if most_recent_node_list:
        # Remove address of current node from list
        current_address = 'http://127.0.0.1:'+str(app.state.port)
        node_list = most_recent_node_list.json()
        node_list.remove(current_address)
        app.state.node_list = node_list

def update_command_blockchain(command_node_address):
    command_node_update_url = command_node_address + "/update-command-blockchain"
    requests.post(command_node_update_url, json=jsonable_encoder(app.state.blockchain.chain))