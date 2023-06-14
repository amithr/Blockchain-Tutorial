from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from blockchain_logic.Blockchain import Blockchain
import requests
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
app.state.logger = None

@app.on_event("startup")
async def startup_event():
    app.state.blockchain = Blockchain()

@app.post('/initialize-command-node')
async def initialize_command_node(data: Request):
    data = await data.json()
    user_id = data['user_id']
    port = data['port']
    node_id = data['node_id']
    app.state.logger = Logger(user_id, port, node_id)
    app.state.logger.emit_log("Command node online.", log_constants.SUCCESS)
    return

@app.post("/initialize-node-blockchain")
def initialize_node_blockchain():
    return jsonable_encoder(app.state.blockchain.chain)

@app.post("/initialize-node-list")
def initialize_node_list(request : Request):
    return jsonable_encoder(app.state.node_list)

@app.post('/update-command-node-list')
async def update_command_node_list(node_address:Request):
    node_address = await node_address.json()
    app.state.node_list.add(node_address)
    app.state.logger.emit_log(node_address + ' added to command node list.', log_constants.UPDATE)


# Receive new blockchain after block
@app.post('/update-command-blockchain')
async def update_command_blockchain(blockchain:Request):
    blockchain = await blockchain.json()
    app.state.blockchain = convert_json_to_blockchain(blockchain)
    # Send purely the array that contains the blockchain data to the logging node
    requests.post("http://127.0.0.1:9001/broadcast-blockchain", json=jsonable_encoder(app.state.blockchain.chain))
    app.state.logger.emit_log('Command blockchain updated.', log_constants.UPDATE)
    print("Node Update", app.state.blockchain.__repr__())