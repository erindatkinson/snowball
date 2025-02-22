"""time functions"""

from dateutil.relativedelta import relativedelta


def duration_printer(duration: relativedelta) -> str:
    """print duration"""
    output = []
    attrs = ["years", "months", "days", "minutes", "seconds"]
    for this_attr in attrs:
        this_value = getattr(duration, this_attr)
        if this_value != 0:
            output.append(f"{abs(this_value)} {this_attr}")
    return " ".join(output)
