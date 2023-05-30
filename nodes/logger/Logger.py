import requests
from fastapi.encoders import jsonable_encoder
from .Log import Log

class Logger:
    def __init__(self, logger_address, node_address=None, node_id=None):
        self.logger_address = logger_address
        self.node_address = node_address
        self.node_id = node_id
    
    def emit_log(self, msg, type):
        log = Log(self.node_address, self.node_id, msg, type)
        try:
            requests.post(self.logger_address, json=jsonable_encoder(log.to_dict()))
        except:
            pass
        print(log)