import React, {FC, useContext, useState, useEffect} from 'react'
import ReactDOM from 'react-dom/client';
import { UserContext } from '../contexts/UserContext';
import { Grid, Button, ButtonGroup, ListItem, List } from '@mui/material';
import { networkAction } from '../utilities/API';
import useWebSocket, { ReadyState } from 'react-use-websocket';

interface DashboardProps {
    userId?:string;
}

const Dashboard: FC<DashboardProps> = () => {
    const {userData, setUserData} = useContext(UserContext);
    const [commandNode, setCommandNode] = useState(8000);
    const [nodes, setNodes] = useState([])
    const [socketUrl, setSocketUrl] = useState('ws://localhost:9001/logging');
    const [messageHistory, setMessageHistory] = useState([]);
    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

    useEffect(() => {
        if (lastMessage !== null) {
          setMessageHistory((prev) => prev.concat(lastMessage));
        }
      }, []);

      const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
      }[readyState];

    const handleGenerateNetwork = () => {
        networkAction('generate_network', {'user_id':userData.email}).then(function(success) {
            setCommandNode(success.data.port)
            setNodes([...nodes, commandNode])
        }).catch(function(error) {
            console.log(error)
        })
    }

    const handleAddMiningNode = () => {
        networkAction('add_mining_node', {'user_id':userData.email, 'command_node_port':commandNode}).then(function(success) {
            console.log("New mining node added");
            const new_node_port = success.data.port
            console.log(new_node_port)
            setNodes([...nodes, new_node_port])
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
                    <span>The WebSocket is currently {connectionStatus}</span>
                    {lastMessage ? <span>Last message: {lastMessage.data}</span> : null}
                    <ul>
                        {messageHistory.map((message, idx) => (
                        <span key={idx}>{message ? message.data : null}</span>
                    ))}
                </ul>
                </Grid>
                <Grid item xs={4}>
                    <h2>Node Statuses</h2>
                </Grid>
            </Grid>
        </>
    );
};
export default Dashboard;