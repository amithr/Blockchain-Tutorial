import React, {FC, useContext, useState, useEffect, useReducer} from 'react'

export const useWebSocket = (url, onMessage) => {
    useEffect(() => {
      const ws = new WebSocket(url);
      ws.onmessage = onMessage;
      return () => {
        ws.close();
      };
    }, []);
};