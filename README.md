# Welcome to the Blockchain Playground!

This is an application that is meant to allow education to demonstrate the functionality of a blockchain voting system in real-time. It is still in active development. It uses Python with numerous FastAPI-based nodes on the backend and React/Typescript in the frontend

## Todos
- Tests (Frontend and Backend)
- React Voting Functionality
- Reducers and Contexts to simplify React Dashboard

## Getting Started
To start the backend:
`sudo uvicorn dashboard_node:app --port=9000`
To start the frontend:
`npm run dev`  

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
![Voting Lifecycle](https://github.com/amithr/Blockchain-Tutorial/blob/main/Voting_Lifecycle.png)

## How does it work?

![Network Overview](https://github.com/amithr/Blockchain-Tutorial/blob/main/Blockchain_Topology.png)
