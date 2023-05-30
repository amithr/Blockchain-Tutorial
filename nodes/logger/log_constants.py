# Emoji symbols
WARNING_EMO = "\u26A0"
SUCCESS_EMO = "\u2713"
UPDATE_EMO = "\U0001F506"
RECEIVED_EMO = "\U0001F4BC"
ERROR_EMO = "\U0001F6A8"

# Warning Types
WARNING = "warning"
SUCCESS = "success"
UPDATE = "update"
RECEIVED = "received"
ERROR = "error"

def get_log_emoji(type):
    if type == "warning":
        return WARNING_EMO
    elif type == "success":
        return SUCCESS_EMO
    elif type == "update":
        return UPDATE_EMO
    elif type == "received":
        return RECEIVED_EMO
    elif type == "error":
        return ERROR_EMO
    