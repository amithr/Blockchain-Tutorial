from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Block import Block
from Blockchain import Blockchain
from blockchain_helpers import blockchain_validation
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.state.node_address = "http://127.0.0.1:5001"

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
    print("Primary Node Update Chain", json_chain)
    requests.post(update_url, json=json_chain)

@app.on_event("startup")
async def startup_event():
    app.state.blockchain = Blockchain()
    update_node_blockchain()



@app.post("/new-transaction-request")
async def receive_new_transaction(transaction : Request):
    transaction = await transaction.json()
    new_block = app.state.blockchain.mine_block(transaction)
    json_new_block = jsonable_encoder(new_block)
    print("New Transaction Request Block", json_new_block)
    if is_consensual(json_new_block):
        print("Is Consensual (Primary Node)")
        app.state.blockchain.add_block_to_blockchain(new_block)

    return JSONResponse(content=json_new_block)


def is_consensual(json_new_block):
    consent_url = app.state.node_address + '/give-consent'
    response = requests.post(consent_url, json=json_new_block).json()
    if not response["valid"] == True:
        return False
    return True