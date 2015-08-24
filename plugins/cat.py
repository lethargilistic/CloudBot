"""
cat.py

Retrieve a cat picture from placekitten.com.

The site doesn't have a picture for every possible combination,
but it's a good spread.

Created By:
    - Mike Overby <https://github.com/lethargilistic>

License:
    GPL v3
"""


from cloudbot import hook
import random


MINIMUM_SIZE = 10
MAXIMUM_SIZE = 5000
RANDOM_FLAGS = ["r", "rand", "random", "any"]


def check_size(size_str):
    """ Convert a string size to an int within the max and min picture size.
    :type size_str: str
    """
    size = int(size_str)
    if size < MINIMUM_SIZE:
        size = MINIMUM_SIZE
    elif size > MAXIMUM_SIZE:
        size = MAXIMUM_SIZE
    return size


@hook.command("cat")
def cat(text=None):
    """
    <RANDOM_FLAGS> - return a randomly sized cat picture.
    <length> - retrieve a square cat picture of this <length>
    <length> <width> - retrieve a cat picture of this <length> and <width>
    """
    length = 0
    width = 0

    if text in RANDOM_FLAGS:
        length = random.randint(MINIMUM_SIZE, MAXIMUM_SIZE)
        width = random.randint(MINIMUM_SIZE, MAXIMUM_SIZE)
    else:
        split = text.split(maxsplit=1)

        # If there is a non-digit arg, don't return a link.
        for part in split:
            if not part.isdigit():
                return

        if len(split) == 1:
            # One arg, square size
            length = width = check_size(split[0])
        elif len(split) == 2:
            # Two args, specified length and width
            length = check_size(split[0])
            width = check_size(split[1])
        else:
            return

    # Placekitten doesn't have perfectly square pictures, for some reason.
    if length == width:
        width += 10

    return "https://placekitten.com/" + str(length) + "/" + str(width)
