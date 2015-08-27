"""
placeholder.py

Retrieve a placeholder picture from lorempixum.com.

Created By:
    - Mike Overby <https://github.com/lethargilistic>

License:
    GPL v3
"""


from cloudbot import hook
import random
import requests


MINIMUM_SIZE = 1
MAXIMUM_SIZE = 1920
RANDOM_FLAGS = ["r"]
GRAYSCALE_FLAGS = ["g"]
BASE_URL = "http://www.lorempixum.com/"


def is_grayscale(args):
    if arg[0] == GRAYSCALE_FLAG:
        args.pop(0)
        return True
    return False
        

def validate_size(size_str):
    """ Return true if size_str is a number and within the min and max size.
    :type size_str: str
    """
    if not size_str.isdigit():
        return False
    size = int(size_str)
    return MINIMUM_SIZE <= size <= MAXIMUM_SIZE


def get_basic_url_parts(args):
    """
    :type args:list
    Return the length, width and whether or not is grayscale from the args.

    If first arg is GREYSCALE_FLAG, then the picture should be grayscale.

    If length arg indicates random, generate random length and width.
    
    If length was valid and second arg was number, width is user-specified.
    If length was valid, but second arg was a tag, width = length.
    If length was invalid, returns None, None.

    If an arg is added for length or width or grayscale
    , it is removed from the list, leaving only other args.
    """
    is_gray = False
    if args[0] in GRAYSCALE_FLAGS:
        args.pop(0)
        is_gray = True
        
    if args[0] in RANDOM_FLAGS:
        # If they want a random image, return a random image.
        length = random.randint(MINIMUM_SIZE, MAXIMUM_SIZE)
        width = random.randint(MINIMUM_SIZE, MAXIMUM_SIZE)
        args.pop(0)
    elif validate_size(args[0]):
        #First arg MUST be a valid length.
        length = width = int(args[0])
        args.pop(0) #remove the used arg from the list.
        if len(args) > 0 and validate_size(args[0]):
            #Second arg (first was removed, so 0) may be the width.
            width = int(args[0])
            args.pop(0) #remove the used arg from the list.
    else:
        #The length was invalid. Indicate this.
        length = width = None

    return is_gray, length, width


def create_url(length, width, is_gray):
    """
    :type length: int, numeric string
    :type width: int, numeric string
    Create a basic url with length and width
    """
    url = BASE_URL
    if is_gray:
        url += "g/"
    return url + str(length) + "/" + str(width)


def append_args(length, width, is_gray, args):
    """
    :type length: int, numeric string
    :type width: int, numeric string'
    :type tags: list of strings
    Create a url with length and width, followed by arguments.
    """
    url = create_url(length, width, is_gray)

    if len(args) >= 1:
        if args[0].isalpha():
            # First is always text
            url += "/" + args[0]

    if len(args) >= 2:
        if args[1].isdigit():
            # Second can be selection
            url += "/" + args[1]
        elif args[1].isalpha():
            # Xor, second can be dummy text
            url += "/" + args[1]

    if len(args) >= 3:
        if args[1].isdigit() and args[2].isalpha():
                # If second is selection, third arg can be dummy text
                url += "/" + args[2]
    return url


@hook.command("placeholder", "ph")
def placeholder(text=None):
    """ [g] <r|<length> [width, if different]> [content tag] [<text on image>|<pic number in tag> <text on image>]."""

    """<length> - retrieve a square cat picture of this <length>
    <length> <width> - retrieve a cat picture of this <length> and <width>
    """
    length = None
    width = None
    url = ""
    
    # Split the args up.
    text = text.rstrip()
    split = text.split()

    is_gray, length, width = get_basic_url_parts(split)

    if length is None:
        #The length was invalid. Return nothing.
        return
    
    if 0 < len(split) <= 3:
        # Handle extra args.
        # Split is only the extra args at this point.
        url = append_args(length, width, is_gray, split)
    else:
        # No extra args, just the dimension
        url = create_url(length, width, is_gray) 

    return url
