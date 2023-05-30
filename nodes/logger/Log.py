from .log_constants import get_log_emoji
class Log:
    def __init__(self, node_address, node_id, msg, type):
        self.node_address = node_address
        self.node_id = node_id
        self.msg = msg
        self.type = type
    
    def to_dict(self):
        return {
            "node_address":self.node_address,
            "node_id":self.node_id,
            "msg": self.msg,
            "type": self.type
        }
    
    def __str__(self):
        node_address_string = '['+self.node_address+']'
        node_id = '['+self.node_id+']'
        message = node_address_string + node_id + " "+self.msg+" "+ get_log_emoji(self.type)
        return message
