from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from blockchain_logic.Blockchain import Blockchain
import requests, uvicorn, sys
import requests.exceptions
from node_helper import convert_json_to_blockchain
from logger.Logger import Logger
from logger import log_constants

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is actually a set - ensures that only unique values are added
app.state.node_list = set()
app.state.blockchain = None
app.state.node_count = 0
app.state.logging_node = "http://127.0.0.1:8001"
logger = Logger(app.state.logging_node, "http://127.0.0.1:8000", "Command")

@app.on_event("startup")
async def startup_event():
    app.state.blockchain = Blockchain()
    logger.emit_log("Command node online.", log_constants.SUCCESS)

@app.post("/initialize-identity")
def initialize_identity(request:Request):
    app.state.node_count += 1
    node_address = "http://" + request.client.host + ":" + str(request.client.port)
    identity = {"node_id":str(app.state.node_count), "node_address":node_address}
    return jsonable_encoder(identity)


@app.post("/initialize-node-blockchain")
def initialize_node_blockchain():
    return jsonable_encoder(app.state.blockchain.chain)

@app.post("/initialize-node-list")
def initialize_node_list(request : Request):
    for node_address in app.state.node_list:
        # Ports aren't what they are supposed to be, so we use Docker
        try:
            requests.post(node_address, json=jsonable_encoder(app.state.node_list))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("Command node can't contact child node", node_address)
            continue
        except requests.exceptions.HTTPError:
            print("4xx, 5xx")
            continue
        else:
            print("Child node list updated", node_address)

@app.post('/update-command-node-list')
async def update_command_node_list(node_address:Request):
    node_address = await node_address.json()
    app.state.node_list.add(node_address)
    logger.emit_log(node_address + ' added to command node list.', log_constants.UPDATE)


# Receive new blockchain after block
@app.post('/update-command-blockchain')
async def update_command_blockchain(blockchain:Request):
    blockchain = await blockchain.json()
    app.state.blockchain = convert_json_to_blockchain(blockchain)
    logger.emit_log('Command blockchain updated.', log_constants.UPDATE)
    print("Node Update", app.state.blockchain.__repr__())