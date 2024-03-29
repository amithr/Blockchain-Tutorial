# Welcome to the Blockchain Playground!

This is an application that is meant to allow educators to demonstrate the functionality of a blockchain voting system in real-time. Users can create their own custom blockchain network and submit votes to it, which are stored on a blockchain. The application is still in active development. It uses Python with numerous FastAPI-based nodes on the backend and React/Typescript on the frontend.

# Table of Contents
1. [Getting Started](#getting-started)
2. [User Guide](#user-guide-smirk_cat)
3. [How does it work?](#how-does-it-work-sparkles)
4. [Components (Nodes & Frontend)](#components)
5. [What happens when someone votes?](#what-happens-when-someone-votes-raising_hand)
6. [API](#api-zap)
7. [Troubleshooting](#troubleshooting-mag_right)

## Todos
- [ ] Functional Tests (Frontend and Backend)
- [ ] React Voting Functionality
- [ ] Reducers and Contexts to simplify React Dashboard

## Getting Started
To set up the frontend:
1. `cd blockchain-voter-dashboard`
2. `npm install`

To set up the backend:
`pip install -r requirements.txt`

To start the backend:
1. Open up a new terminal window
2. `cd nodes`
3. `sudo uvicorn dashboard_node:app --port=9000`

To start the frontend:
1. Open up a new terminal window (separate from the backend)
2. `cd blockchain-voter-dashboard`
3. `npm run dev`

To test backend voting functionality:
1. Open up a new terminal window (separate from the backend and frontend)
2. `pytest test_node_api.py`

## User Guide :smirk_cat:
1. Access the dashboard's login page at http://localhost:5173
2. Click the "Sign in with Google" button and follow the login prompts. Afterwards you will be directed to the dashboard.
3. Click the "Generate Network" button and wait until you see the "Command node online." ,message in the Activity Dashboard section.
4. Click the "Add Mining Node" button twice to create two new mining nodes. You should see two messages in the Activity dashboard that read "Mining node online and initialized."
5. Simulate a vote by running `pytest test_node_api.py` from the main directory. You should see a series of steps in your activity dashbaord that correspond to the mining and approval process as well as the first block of the blockchain in the "Blockchain" section.

## Directory Structure :file_folder:
There are 3 main directions:
- **/blockchain-voter-dashboard** [React frontend]
- **/nodes** [All blockchain and network-related code]
	- **/blockchain_logic**
		- **/blockchain_helpers**
			- *Block.py* [Individual Block class]
			- *Blockchain.py* [Blockchain class]
	- **/logger** [Used to generate logs]
		- *dashboard_node.py* [Interfaces with frontend, used to generate network]
		- *logging_node.py* [Collects log messages and sends to frontend via websockets]
		- *command_node.py* [Controls and updates network with new info]
		- *mining_node.py* [Responsible for creating new blocks and updating blockchain]
- **/voting_client** [Desktop-based frontend]

## How does it work? :sparkles:
### Summary
- The application will be launched with a dashboard node, a logging node, and a React frontend.
- Each node is a purpose-specific API server that sends and receives requests.
- The code that provides each node its functionality is based on a Python web framework
called FastAPI. However, a piece of software called Uvicorn is the web server that actually executes and allows requests to be made to your FastAPI code from the internet.
- All nodes are stored on a single machine and will have the same IP address, however, each node has a unique port number assigned to it.
- Nodes can only be manually stopped and started via the dashboard node's API.
- Each user must create a command node and mining nodes to have functional blockchain network. This can be done from the dashboard in the frontend.
- Once a network is established, votes can be submitted to any one of the user's mining nodes and a blockchain will begin to be built. Votes can be be submitted via the dashboard.
### Components
To better understand how the application works, let's take a look at the roles played by all the active components in the application.
#### Frontend
- Allows user to send request to dashboard node to initiate the creation of new networks (command nodes)
- Allows user to send request to dashboard node to add mining nodes to the network
- Receives and displays real-time telemetry regarding status of network nodes and the blockchain 
- Allows user to submit votes to blockchain network. (Will allow user to send links to voters in future.)
#### Dashboard Node
- Intermediary between the frontend and the numerous command and mining nodes
- Creates single logging node on startup that receives all log messages
- Initiates creation of command node for each user (on request from frontend)
- Initiates creation of mining nodes in individual users' networks (on request from frontend)
#### Command Node
- Linked to individual user
- Stores current blockchain
- Stores list of all nodes associated with user's network
#### Mining Node
- Accepts vote and generates new block for each vote via mining process
- Adds block to current blockchain
- Approves new blocks generated by other nodes
- If receiving vote, updates command node with new blockchain
#### Logging Node
- Receives status updates from entire network
- When status update received, pushes update via websockets to user's web browser
  
The diagram below illustrates the above nodes and their roles :point_down:

![Network Overview](https://github.com/amithr/Blockchain-Tutorial/blob/main/Blockchain_Topology.png)

## What happens when someone votes? :raising_hand:
1. The vote is sent from the frontend dashboard to one of the mining nodes - the specific mining node is selected at random.
2. The mining node "mines" or creates a block that stores the vote.
3. This mining node send this newly created block to all the other mining nodes in the network
4. If authentic, this block is added to the blockchains on each of the mining nodes.
5. Each of the mining nodes sends a confirmation of authenticity to the original mining node that received the vote.
6. The newly created block is added to the blockchain on the original mining node.
7. The original mining node sends the new blockchain to the command node, which then updates its own copy of the current blockchain.
   
The diagram below illustrates this process :point_down:

![Voting Lifecycle](https://github.com/amithr/Blockchain-Tutorial/blob/main/Voting_Lifecycle.png)

## API :zap:
To start and stop individual nodes and networks, the main point of access will be the
API routes of the dashboard node.
### Starting a Network
"/new-network" (user_id)

`curl -X POST -H "Content-Type: application/json" -d '{"user_id": <user-google-login-id>}' -L https://<machine-ip-address>/new-network`

**user-google-login-id** - User's login id provided by Google API

**machine-ip-address** - the IP address of the machine on which your application is running; if requests are executed locally, this may simply be 127.0.0.1

Response: 
{'port':command_node_port, 'id': command_node_id}

'port' - port number of new command node
'id' - id number of new command node
### Starting Mining Nodes
"/new-mining-node" (command_node_port, user_id)

`curl -X POST -H "Content-Type: application/json" -d '{"command_node_port": <command-node-port>, "user_id": <user-google-login-id>}' -L https://<machine-ip-address>/new-mining-node`

**command-node-port** - the port of the command node for the user's network; obtained as an API response when network was created

Response:
{'port':port}

'port' - port of new mining node

### Killing Nodes
"/kill-node" (port)

`curl -X POST -H "Content-Type: application/json" -d '{"port": <port>, "user_id": <user-google-login-id>}' -L https://<machine-ip-address>/kill-node`

**port** - port number of node to kill

Response:
{'port':port}

'port' - port number of node killed

## Troubleshooting :mag_right:
### Application Events :high_brightness:
Troubleshooting in the Blockchain-Tutorial is relatively easy because of detailed logging.

In order to detect the source of an error on the backend or frontend, simply open the respective terminal window/tab.

Different events generated by the application, including error events, will be displayed in the following format:
```[<IP-address>:<Port>][<Node-number>][<Message>]```

### "INFO:" Messages :envelope:
These are logs generated by the FastAPI framework running on each node. They usually start with the text "INFO:" and then display the machine's IP address followed by a message indicating an interaction with the node's API.

They are displayed in the following format:

```INFO:	<IP-address>:<Port> - <API Request Method><URL Handle>HTTP 1.1<Status Code>```

These IP addresses with 5-digit port numbers are known as "ephemeral",
as a new port number is created for each API interaction. As a result, these are difficult to attribute to specific nodes and are therefore not useful for troubleshooting.

See a snapshot from a backend terminal window below for context :point_down:

![Troubleshooting](https://github.com/amithr/Blockchain-Tutorial/blob/main/Troubleshooting_2.png)
