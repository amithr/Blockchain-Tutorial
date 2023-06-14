import React, {FC, useContext, useState, useEffect, useLayoutEffect} from 'react'
import { UserContext } from '../contexts/UserContext';
import { Grid, Button, ButtonGroup, ListItem, List } from '@mui/material';
import { networkAction } from '../utilities/API';
import io from 'socket.io-client';

interface DashboardProps {
    userId?:string;
}

const Dashboard: FC<DashboardProps> = () => {
    const {userData, setUserData} = useContext(UserContext);
    const [commandNode, setCommandNode] = useState(8000);
    const [messages, setMessages] = useState([]);
    const [blockchain, setBlockchain] = useState([])
    const [prevMessage, setPrevMessage] = useState("");
    const [nodes, setNodes] = useState([])


    useLayoutEffect(() => {
        // connect to WebSocket server
        const ws = new WebSocket("ws://localhost:9001/logger")
        ws.onmessage = (ev:any) => {
            const message = JSON.parse(ev.data).lastMessage
            setPrevMessage(prev => {
                if (message !== prev) {
                  setMessages(current => [...current, message]);
                }
                return message;
              });
          }
      }, [prevMessage]);

      useLayoutEffect(() => {
        // connect to WebSocket server
        const ws = new WebSocket("ws://localhost:9001/blockchain");
        ws.onmessage = (ev: any) => {
          const blockchainArray = JSON.parse(ev.data).blockchain;
          console.log("Blockchain Array" + blockchainArray)
          setBlockchain(blockchainArray);
        };
      }, []);

    const handleGenerateNetwork = () => {
        networkAction('generate_network', {'user_id':userData.email}).then(function(success) {
            setCommandNode(success.data.port)
            setNodes(nodes => [...nodes, commandNode])
        }).catch(function(error) {
            console.log(error)
        })
    }

    const handleAddMiningNode = () => {
        networkAction('add_mining_node', {'user_id':userData.email, 'command_node_port':commandNode}).then(function(success) {
            console.log("New mining node added");
            const new_node_port = success.data.port
            console.log(new_node_port)
            setNodes(nodes => [...nodes, new_node_port])
        }).catch(function(error) {
            console.log(error)
        })
    }

    const handleKillNode = (port:number) => {
        networkAction('kill_mining_node', {'port':port}).then(function(success) {
            nodes.filter((node) => node !== port);
            console.log('Node successfully killed.')
        }).catch(function(error) {
            console.log(error)
        })
    }

    const handleKillNetwork = () => {
        networkAction('kill_mining_node', {'port':commandNode}).then(function(success) {
            console.log('Node successfully killed.')
        }).catch(function(error) {
            console.log(error)
        })
        for(var node in nodes) {
            networkAction('kill_mining_node', {'port':node})
        }
    }

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
                    <List>
                        {messages.map((message, index) => (
                            <ListItem key={index}>{message}</ListItem>
                        ))}
                    </List>
                </Grid>
                <Grid item xs={4}>
                    <h2>Blockchain</h2>
                    {blockchain.map((block, index) => (
                            <ListItem key={index}>{block.timestamp}</ListItem>
                        ))}
                </Grid>
            </Grid>
        </>
    );
};
export default Dashboard;