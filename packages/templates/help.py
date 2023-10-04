"""module for help string template"""

help_string = """
## Snowball-bot

A discord bot to enable a shared, sisyphean task of "number go up"

- Valid countings
 - Message that is just an integer of the expected next count `eg. (1, 2, 3, 4, etc.)`
 - Reverse Polish Notation math that resolves to the expected next count `eg. _3 4 + 12 9 - -` 
- Invalid countings
 - Message that is just an integer not of the expected next count
 - Reverse Polish Notation math that does not resolves to the expected next count
- Ignored messaged
 - Any message that doesn't start with either a digit or an underscore (dc uses `_` for negative numbers)

See [docs](https://github.com/erindatkinson/snowball#counting) for more details.
"""
