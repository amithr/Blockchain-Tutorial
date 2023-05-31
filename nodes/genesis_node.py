# Allows us to create command node and any new nodes
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from logger.Logger import Logger
from logger import log_constants
import uvicorn, requests

app = FastAPI()

origins = ["*"]

app.state.command_node = "http://127.0.0.1:8000"
app.state.logging_node = "http://127.0.0.1:8001"
logger = Logger(app.state.logging_node, "http://127.0.0.1:8005", "Genesis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.emit_log("Genesis node online.", log_constants.SUCCESS)

@app.post("/new-command-node")
def new_command_node():
    uvicorn.run("command_node:app", port=8000, log_level="info")

@app.post("/new-mining_node")
def new_mining_node(port:int):
    node_address = "http://127.0.0.1:"+str(port)
    command_node_update_address = app.state.command_node + '/update-command-node-list'
    try:
                requests.post(command_node_update_address, json=jsonable_encoder(node_address))
    except:
        logger.emit_log("Failed to update command node node list with new port", log_constants.ERROR)
    else:
        uvicorn.run("mining_node:app", port=port, log_level="info")