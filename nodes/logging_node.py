from fastapi import FastAPI, Request, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from logger.Logger import Logger
from logger import log_constants
import asyncio, websockets

app = FastAPI()
app.state.last_message = ""

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/logger")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            await asyncio.sleep(1)
            await websocket.send_json(jsonable_encoder({'lastMessage': app.state.last_message}))
        except:
             print('Waiting for connection')
             break


@app.post("/broadcast-message")
async def broadcast_message(msg:Request):
    # Need to wait for one second to let any other requests be sent
    await asyncio.sleep(1)
    msg = await msg.json()
    app.state.last_message = msg