from .log_constants import get_log_emoji
class Log:
    def __init__(self, user_id, port, node_id, msg, type):
        self.user_id = user_id
        self.node_address = "http://127.0.0.1:"+str(port)
        self.node_id = node_id
        self.msg = msg
        self.type = type
    
    def to_dict(self):
        return {
            "user_id":self.user_id,
            "node_address":self.node_address,
            "node_id":self.node_id,
            "msg": self.msg,
            "type": self.type
        }
    
    def __str__(self):
        node_address_string = '['+self.node_address+']'
        node_id = '['+str(self.node_id)+']'
        message = node_address_string + str(node_id) + " "+self.msg+" "+ get_log_emoji(self.type)
        return message
