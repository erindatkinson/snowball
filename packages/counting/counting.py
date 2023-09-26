"""module maaging counting state"""

def check_next_count(message:str) -> bool:
    """check if the message is valid for the next expected count"""
    return isinstance(message, str)

def increment_count()->None:
    """update the state of the expected count to the next iteration"""

def reset_count()->None:
    """reset the state of the expected count back to the beginning"""
