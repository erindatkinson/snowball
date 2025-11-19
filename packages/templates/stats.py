"""module for reset templates"""

# If you have more successes


def success(year, data):
    """for printing the success message"""

    react_string = (
        REACT_NINE_MESSAGE.format(react_nine=data["given9-s"])
        if data["given9-s"] > 0
        else ""
    )

    return (
        SUCCESS_MESSAGE.format(
            year=year, successes=data["success-s"], failures=data["failure-s"]
        )
        + NINES_MESSAGE.format(count_nine=data["count9-s"], react_string=react_string)
        + END_MESSAGE
    )


def struggle(year, data):
    """for printing the struggling message"""
    react_string = (
        REACT_NINE_MESSAGE.format(react_nine=data["given9-s"])
        if data["given9-s"] > 0
        else ""
    )
    return (
        STRUGGLE_MESSAGE.format(
            year=year, successes=data["success-s"], failures=data["failure-s"]
        )
        + NINES_MESSAGE.format(count_nine=data["count9-s"], react_string=react_string)
        + END_MESSAGE
    )


SUCCESS_MESSAGE = """OMG you were a counting rockstar in {year}

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

You successfully counted {successes} times 🤯

"""

STRUGGLE_MESSAGE = """You worked hard counting in {year} 💜

📈📈📈📈📈📈📈📈📈📈📈📈

You had a total of {successes} successful counts! 

"""

NINES_MESSAGE = """🟪9️⃣🟪9️⃣🟪9️⃣🟪9️⃣🟪9️⃣🟪9️⃣
9️⃣🟪9️⃣🟪9️⃣🟪9️⃣🟪9️⃣🟪9️⃣🟪

It's always a fine times for nines! And you
showed how it's done by counting with 9s
a whole {count_nine} times{react_string}
"""

END_MESSAGE = """
💜💜💜💜💜💜💜💜💜💜💜💜

We are all counting dreamers, だってばよ!
All the best for another year of counting.
[.](https://raw.githubusercontent.com/erindatkinson/snowball/refs/heads/main/assets/winter-landscape-4532412_1280.jpg)"""


REACT_NINE_MESSAGE = """ and received the love of
nines with {react_nine} 9️⃣s given to you"""
