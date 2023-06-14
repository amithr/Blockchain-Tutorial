from fastapi import FastAPI, Request, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from logger.Logger import Logger
from logger import log_constants
import asyncio, websockets
from node_helper import convert_json_to_blockchain

app = FastAPI()
app.state.last_message = ""
app.state.blockchain = []

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/blockchain")
async def websocket_blockchain_endpoint(websocket: WebSocket):
    print('Accepting requests for blockchain updates...')
    await websocket.accept()
    
    # Store the initial state of the blockchain
    prev_blockchain = app.state.blockchain.copy()
    
    while True:
        await asyncio.sleep(1)
        
        # Check if the blockchain state has changed
        if app.state.blockchain != prev_blockchain:
            await websocket.send_json(jsonable_encoder({'blockchain': app.state.blockchain}))
            prev_blockchain = app.state.blockchain.copy()



@app.websocket("/logger")
async def websocket_logger_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    
    # Store the initial value of last_message
    prev_last_message = app.state.last_message
    
    while True:
        await asyncio.sleep(1)
        
        # Check if last_message has changed
        if app.state.last_message != prev_last_message:
            await websocket.send_json(jsonable_encoder({'lastMessage': app.state.last_message}))
            prev_last_message = app.state.last_message

@app.post("/broadcast-blockchain")
async def broadcast_blockchain(blockchain:Request):
    blockchain = await blockchain.json()
    app.state.blockchain = blockchain


@app.post("/broadcast-message")
async def broadcast_message(msg:Request):
    # Need to wait for one second to let any other requests be sent
    await asyncio.sleep(1)
    msg = await msg.json()
    app.state.last_message = msg