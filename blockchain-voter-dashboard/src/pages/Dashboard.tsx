import React, {FC, useContext, useState, useEffect, useReducer} from 'react';
import NetworkStatusFeed from '../components/NetworkStatusFeed';
import BlockchainStatusFeed from '../components/BlockchainStatusFeed';
import { nodeReducer } from '../hooks/nodeReducer';
import { useWebSocket } from '../hooks/useWebsocket';
import { UserContext } from '../contexts/UserContext';
import { Grid, Button, ButtonGroup, ListItem, List } from '@mui/material';
import { networkAction } from '../utilities/API';

interface DashboardProps {
    userId?:string;
}

const initialState = {
    commandNode: 8000,
    messages: [],
    blockchain: [],
    prevMessage: '',
    nodes: [],
};

const Dashboard: FC<DashboardProps> = () => {
    const {userData, setUserData} = useContext(UserContext);
    const [state, dispatch] = useReducer(nodeReducer, initialState);
    const {commandNode, messages, blockchain, prevMessage, nodes } = state;

    useWebSocket('ws://localhost:9001/logger', (ev) => {
        const message = JSON.parse(ev.data).lastMessage;
        dispatch({ type: 'SET_PREV_MESSAGE', payload: message });
        if (message !== prevMessage) {
            dispatch({ type: 'ADD_MESSAGE', payload: message });
        }
    });

    // WebSocket connection for blockchain
    useWebSocket('ws://localhost:9001/blockchain', (ev) => {
        const blockchainArray = JSON.parse(ev.data).blockchain;
        dispatch({ type: 'SET_BLOCKCHAIN', payload: blockchainArray });
    });

    const handleGenerateNetwork = () => {
        networkAction('generate_network', { user_id: userData.email })
          .then((success) => {
            const commandNodePort = success.data.port;
            dispatch({ type: 'SET_COMMAND_NODE', payload: commandNodePort });
            dispatch({ type: 'ADD_NODE', payload: commandNodePort });
          })
          .catch((error) => {
            console.log(error);
          });
      };

      const handleAddMiningNode = () => {
        networkAction('add_mining_node', {
          user_id: userData.email,
          command_node_port: commandNode,
        })
          .then((success) => {
            const newMiningNodePort = success.data.port;
            console.log(newMiningNodePort);
            dispatch({ type: 'ADD_NODE', payload: newMiningNodePort });
          })
          .catch((error) => {
          });
      };

    const handleKillNode = (port:number) => {
        networkAction('kill_mining_node', {'port':port}).then(function(success) {
            nodes.filter((node) => node !== port);
        }).catch(function(error) {
        })
    }

    const handleKillNetwork = () => {
        networkAction('kill_mining_node', { port: commandNode })
          .then((success) => {
          })
          .catch((error) => {
          });
    
        nodes.forEach((node) => {
          networkAction('kill_mining_node', { port: node });
        });
      };
    

    return(
        <>
            <Grid container spacing={2}>
                <Grid item xs={4}>
                    <h2>Control Panel for {userData.email}</h2>
                    <ButtonGroup orientation="vertical"
                            aria-label="vertical outlined button group">
                        <Button onClick={() => {handleGenerateNetwork();}}>Generate Network</Button>
                        <Button onClick={() => {handleAddMiningNode();}}>Add Mining Node</Button>
                        <Button>Kill Mining Node</Button>
                        <Button onClick={() => {handleKillNetwork();}}>Kill Network</Button>
                        <Button>Take a Vote</Button>
                    </ButtonGroup>
                    <List>
                        {nodes.map((node, index) => (
                            <ListItem key={index}>Node {index}: {node}</ListItem>
                        ))}
                    </List>
                </Grid>
                <Grid item xs={4}>
                    <h2>Activity Dashboard</h2>
                    <NetworkStatusFeed messages={messages} />
                </Grid>
                <Grid item xs={4}>
                    <h2>Blockchain</h2>
                    <BlockchainStatusFeed blockchain={blockchain} />
                </Grid>
            </Grid>
        </>
    );
};
export default Dashboard;