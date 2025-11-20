"""module for running stats"""

from discord import Message

OUTPUT_KEYS = ["chatting", "given9", "failure", "success", "count9", "command"]


def process_message(message: Message) -> dict:
    """Create countable dict from message"""
    out = {k: False for k in OUTPUT_KEYS}

    if len(message.content) > 0 and message.content[0] == "!":
        out["command"] = True
    elif "9" in message.content:
        out["count9"] = True

    attempted_count = False
    for reaction in message.reactions:
        if reaction.emoji == "✅" and reaction.me:
            attempted_count = True
            out["success"] = True
        elif reaction.emoji == "❎" and reaction.me:
            attempted_count = True
            out["failure"] = True
        elif reaction.emoji == "9️⃣":
            out["given9"] = True
        elif reaction.emoji in ["🌨", "🎭"]:
            attempted_count = True

    if not attempted_count and not out["command"]:
        out["chatting"] = True

    return out


def coalesce(out, data):
    """coalesce data into a single dict"""

    for key in data.keys():
        if data[key]:
            out[f"{key}-s"] += 1
    return out
