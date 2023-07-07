import React, {FC, useContext, useState, useEffect, useLayoutEffect} from 'react';
import { Grid, Button, ButtonGroup, ListItem, List } from '@mui/material';

type NetworkStatusFeedProps = {
    messages:[];

}

const NetworkStatusFeed: FC<NetworkStatusFeedProps> = ({messages}) => {
    return(
        <>
            <List>
                {messages.map((message, index) => (
                    <ListItem key={index}>Node {index}: {message}</ListItem>
                ))}
            </List>
        </>
    );
};

export default NetworkStatusFeed;