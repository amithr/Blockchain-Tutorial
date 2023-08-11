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
5. Each of the mining nodes sends a confirmation response to the original mining node that received the vote.
6. The newly created block is added to the blockchain on the original mining node.
7. The original mining node sends the new blockchain to the command node, which then updates its own copy of the current blockchain.

![Voting Lifecycle](https://github.com/amithr/Blockchain-Tutorial/blob/main/Voting_Lifecycle.png)

## How does it work?

![Network Overview](https://github.com/amithr/Blockchain-Tutorial/blob/main/Blockchain_Topology.png)

## User Guide