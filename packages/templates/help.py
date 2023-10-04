"""module for help string template"""

help_string = """
## Snowball-bot

A discord bot to enable a shared, sisyphean task of "number go up"

Each player can take a turn posting the next expected integer in this channel, if correct, 
the post will be marked by the bot with a ✅. If incorrect, the post will be marked by the bot
with a ❎. There are some cases where players may post at the same time, in this case, one player
will 'lock' the guess in and the other player's guess will not count. In this case, the uncounted
player's post will be marked with a 🌨. While you may want to play on your own, that's not the intent
of this bot currently, and so if you post twice in a row, the guess will not count and your post will
be marked with a 🎭. If the bot goes down for any reason and your guesses were not captured, when the
bot comes back up, it will announce that it is up and what the last valid count was.

Guesses can be in the form of the expected number itself, eg. `1`, `2`, etc. or with math. This bot
only allows reverse polish notation (also known as postfix notation) math equations. If you'd like
to write a solid string parsing infix calculator in python we're accepting PRs, but until then, the
author of this bot was lazy and postfix was less work to manage. Some examples of postfix notation math
are as follows: if the expected number is 32, you would be able to write `2 3 ^ 4 *` (which would be akin
to 2^3 * 4 with infix notation), or if the expected number is 1, you could write `_3 _3 * 16 2 / -` (which
would be like writing `( -3 * -3 ) - ( 16 / 2 )` with infix)
"""
