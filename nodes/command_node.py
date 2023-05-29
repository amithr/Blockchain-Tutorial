from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from blockchain_logic.Blockchain import Blockchain
import requests
import requests.exceptions


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
app.state.node_list = {"http://127.0.0.1:5002", "http://127.0.0.1:5003"}
app.state.blockchain = None

@app.on_event("startup")
async def startup_event():
    app.state.blockchain = Blockchain()
    print("Command node online")


@app.post("/initialize-node-blockchain")
def initialize_node_blockchain():
    return jsonable_encoder(app.state.blockchain.chain)

@app.post("/initialize-node-list")
def initialize_node_list(request : Request):
    # Make a copy of old node list
    # Get address of most recent node
    # Add new node address to node list
    # Update all the nodes on the old list with the new list
    # Return old node list
    old_node_list = app.state.node_list.copy()
    new_node_address = "http://" + request.client.host + ":" + str(request.client.port)
    print("New node address", new_node_address)
    app.state.node_list.add(new_node_address)
    print("Command Node node list", app.state.node_list)
    for node_address in old_node_list:
        # Ports aren't what they are supposed to be
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
    return jsonable_encoder(old_node_list)

@app.post('/update-command-blockchain')
def update_command_blockchain(blockchain:Request):
    return