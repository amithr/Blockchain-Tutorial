# Welcome to the Blockchain Playground!

This is an application that is meant to allow educators to demonstrate the functionality of a blockchain voting system in real-time. It is still in active development. It uses Python with numerous FastAPI-based nodes on the backend and React/Typescript on the frontend

## Todos
- Functional Tests (Frontend and Backend)
- React Voting Functionality
- Reducers and Contexts to simplify React Dashboard

## Getting Started
To set up the frontend:
1. `cd blockchain-voter-dashboard`
2. `npm install`

To set up the backend:
`pip install -r requirements.txt`

To start the backend:
`sudo uvicorn dashboard_node:app --port=9000`

To start the frontend:
`npm run dev` 

To test backend voting functionality:
`pytest test_node_api.py`

## Directory Structure
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

## What happens when someone votes?
1. The vote is sent from the frontend dashboard to one of the mining nodes - the specific mining node is selected at random.
2. The mining node "mines" or creates a block that stores the vote.
3. This mining node send this newly created block to all the other mining nodes in the network
4. If authentic, this block is added to the blockchains on each of the mining nodes.
5. Each of the mining nodes sends a confirmation of authenticity to the original mining node that received the vote.
6. The newly created block is added to the blockchain on the original mining node.
7. The original mining node sends the new blockchain to the command node, which then updates its own copy of the current blockchain.
   
The diagram below illustrates this process :point_down:

![Voting Lifecycle](https://github.com/amithr/Blockchain-Tutorial/blob/main/Voting_Lifecycle.png)

## How does it work?
To understand how the application works, let's take a look at the roles played by all the active components in application.
### Frontend
- Allows user to send request to dashboard node to initiate the creation of new networks (command nodes)
- Allows user to send request to dashboard node to add mining nodes to the network
- Receives and displays real-time telemetry regarding status of network nodes and the blockchain 
### Dashboard Node
- Intermediary between the frontend and the numerous command and mining nodes
- Creates single logging node on startup that receives all log messages
- Initiates creation of command node for each user (on request from frontend)
- Initiate creation of mining nodes in individual users' networks (on request from frontend)
### Command Node
- Linked to individual user
- Stores current blockchain
- Stores list of all nodes associated with user's network
### Mining Node
- Accepts vote and generates new block for each vote via mining process
- Adds block to current blockchain
- Approves new blocks generated by other nodes
- If receiving vote, updates command node with new blockchain
### Logging Node
- Receives status updates from entire network
- When status update received, pushes update via websockets to user's web browser
  
  The diagram below illustrates the above nodes and their roles :point_down:

![Network Overview](https://github.com/amithr/Blockchain-Tutorial/blob/main/Blockchain_Topology.png)

## User Guide
1. Access the dashboard's login page at http://localhost:5173
2. Click the "Sign in with Google" button and follow the login prompts. Afterwards you will be directed to the dashboard.
3. Click the "Generate Network" button and wait until you see the "Command node online." ,message in the Activity Dashboard section.
4. Click the "Add Mining Node" button twice to create two new mining nodes. You should see two messages in the Activity dashboard that read "Mining node online and initialized."
5. Simulate a vote by running `pytest test_node_api.py` from the main directory. You should see a series of steps in your activity dashbaord that correspond to the mining and approval process as well as the first block of the blockchain in the "Blockchain" section.