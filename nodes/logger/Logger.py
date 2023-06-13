import requests
from fastapi.encoders import jsonable_encoder
from .Log import Log

class Logger:
    def __init__(self, user_id, port=None, node_id=None):
        self.user_id = user_id
        self.logger_address = "http://127.0.0.1:9001/broadcast-message"
        self.port = str(port)
        self.node_id = node_id
    
    def emit_log(self, msg, type):
        log = Log(self.user_id, self.port, self.node_id, msg, type)
        try:
            requests.post(self.logger_address, json=jsonable_encoder(log.__str__()))
        except:
            pass
        print(log)