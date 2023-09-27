"""module to manage main interface to the services package"""

from .discord import run

clients = {
    "discord": run,
}
