"""module maaging counting state"""
from subprocess import run, CalledProcessError
from logging import debug

def parse_message(message:str) -> tuple[int, bool]:
    """parses message and uses linux dc to calculate math
    returns a tuple of the value and a bool of if the message was countable"""

    # try to see if the number is just a number
    try:
        count = int(message)
        return (count, True)
    except ValueError:
        debug("message not wholly integer")

    # check if the first character is a digit if not, return not countable
    try:
        int(message[0])
    except ValueError:
        return (-1, False)
    
    # shim out to linux desk calculator to see if message is postfix math
    try:
        data = run(["dc", "-e", message + " p"], capture_output=True, check=True)
        count = int(data.stdout)
        return (count, True)
    except ValueError:
        return (-1, True)
    except CalledProcessError:
        return (-1, True)