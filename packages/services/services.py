"""module to manage main interface to the services package"""

from .discord import new_client
clients = {
    "discord": new_client,
}
