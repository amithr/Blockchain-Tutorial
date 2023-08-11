# Allows us to create command node and any new nodes
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from logger.Logger import Logger
from logger import log_constants
import uvicorn, requests, time
from psutil import process_iter
from signal import SIGTERM # or SIGKILL
import multiprocessing


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.nodes = set()
app.state.initial_port = 8000
app.state.initial_id = 2
# Dashboard node_id will always be 0
# Logger node_id will always be 1
logger = Logger("","http://127.0.0.1:9000", 0)


@app.on_event("startup")
async def startup_event():
    # Create db
    # db.create_database()
    # Create logging node
    p = multiprocessing.Process(target=start_logging_node)
    p.start()
    logger.emit_log("Genesis node online.", log_constants.SUCCESS)

# Update logging node with new websocket handle based on user id
def update_logging_node():
     return

@app.post("/new-network")
async def new_command_node(network_data:Request):
    network_data = await network_data.json()
    user_id = network_data["user_id"]
    print(network_data["user_id"])
    app.state.initial_port += 1
    app.state.initial_id += 1
    command_node_port = app.state.initial_port
    command_node_id = app.state.initial_id
    # Update the logging node
    p = multiprocessing.Process(target=start_command_node, args=(command_node_port,))
    p.start()
    # After 3 seconds, new node should have been created
    time.sleep(3)
    initialize_command_node(user_id, command_node_port, command_node_id)
    return jsonable_encoder({'port':command_node_port, 'id': command_node_id})

def initialize_websocket_channel():
     return

def initialize_command_node(user_id, port, id):
    address = "http://127.0.0.1:" + str(port) + "/initialize-command-node"
    requests.post(address, json=jsonable_encoder({'user_id':user_id, 'port':port, 'node_id':id}))
    return

@app.post("/new-mining-node")
async def new_mining_node(network_data:Request):
    network_data = await network_data.json()
    command_node_port = network_data['command_node_port']
    user_id = network_data['user_id']
    command_node_address = "http://127.0.0.1:" + str(command_node_port)
    app.state.initial_port += 1
    app.state.initial_id += 1
    port = app.state.initial_port
    node_id = app.state.initial_id 
    node_address = "http://127.0.0.1:"+str(port)
    command_node_update_address = command_node_address + '/update-command-node-list'
    try:
                requests.post(command_node_update_address, json=jsonable_encoder(node_address))
    except:
        logger.emit_log("Failed to update command node node list with new port", log_constants.ERROR)
    else:
        p = multiprocessing.Process(target=start_mining_node, args=(port,))
        p.start()
        # After 3 seconds, new node should have been created
        time.sleep(3)
        initialize_mining_node(user_id, command_node_port, port, node_id)
        return jsonable_encoder({'port':port})


def initialize_mining_node(user_id, command_node_port, port, node_id):
    print('User ID:', user_id)
    address = "http://127.0.0.1:" + str(port) + "/initialize-mining-node"
    command_node_address = "http://127.0.0.1:" + str(command_node_port)
    requests.post(address, json=jsonable_encoder({'user_id':user_id, 'command_node_address': command_node_address, 'port':port, 'node_id':node_id}))
    return

@app.post("/kill-node")
async def kill_node(data:Request):
    data = await data.json()
    port = data['port']
    print("Port to Kill:", port)
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == port:
                proc.send_signal(SIGTERM)    
    return jsonable_encoder({'port':port})

@app.post("/kill_network")
def kill_blockchain_network():
     return

     
@app.post("/validate-google-log")
def validate_google_login(token: Request):
     return

# Check health

def start_logging_node():
     uvicorn.run("logging_node:app", port=9001, log_level="info")

def start_command_node(port):
    uvicorn.run("command_node:app", port=port, log_level="info")
    
def start_mining_node(port):
    uvicorn.run("mining_node:app", port=port, log_level="info")