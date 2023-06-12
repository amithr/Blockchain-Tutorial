from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from logger.Logger import Logger
from logger import log_constants
from  fastapi_websocket_pubsub import PubSubEndpoint

app = FastAPI()
endpoint = PubSubEndpoint()
endpoint.register_route(app, "/logging")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/broadcast-message")
async def broadcast_message(msg:Request):
    msg = await msg.json()
    await endpoint.publish(["amith"], data=[msg])
    return