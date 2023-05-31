from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.state.logs = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Logging node online")

@app.post("/log")
async def log(message: Request):
    log_message = message.json()
    app.state.logs.append(log_message)
    print(await message.json())
    return

@app.post("/get_logs")
def get_logs():
    return jsonable_encoder(app.state.logs)

# Use websockets to communicate with logging_node