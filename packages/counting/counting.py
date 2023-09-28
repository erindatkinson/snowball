"""module maaging counting state"""
from subprocess import run, CalledProcessError

def parse_message(message:str) -> tuple[int, bool]:
    """parses message and uses linux dc to calculate math"""
    try:
        int(message[0])
    except ValueError:
        return (-1, False)
    try:
        data = run(["dc", "-e", message + " p"], capture_output=True, check=True)
        count = int(data.stdout)
        return (count, True)
    except ValueError:
        return (-1, True)
    except CalledProcessError:
        return (-1, True)