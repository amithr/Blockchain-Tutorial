import React, {FC, useContext, useState} from 'react'
import ReactDOM from 'react-dom/client';
import { UserContext } from '../contexts/UserContext';
import { Grid, Button, ButtonGroup } from '@mui/material';
import { networkAction } from '../utilities/API';

interface DashboardProps {
    userId?:string;
}

const Dashboard: FC<DashboardProps> = () => {
    const {userData, setUserData} = useContext(UserContext);

    return(
        <>
            <Grid container spacing={2}>
                <Grid item xs={4}>
                    <h2>Control Panel</h2>
                    <ButtonGroup orientation="vertical"
                            aria-label="vertical outlined button group">
                        <Button onClick={() => {networkAction('generate_network');}}
                        
                        >Generate Network</Button>
                        <Button>Add Mining Node</Button>
                        <Button>Kill Mining Node</Button>
                        <Button>Kill Network</Button>
                        <Button>Take a Vote</Button>
                    </ButtonGroup>
                </Grid>
                <Grid item xs={4}>
                    <h2>Activity Dashboard</h2>
                </Grid>
                <Grid item xs={4}>
                    <h2>Node Statuses</h2>
                </Grid>
            </Grid>
            <h2>{userData.email}</h2>
        </>
    );
};
export default Dashboard;