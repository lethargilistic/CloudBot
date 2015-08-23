import re

from cloudbot import hook

from cloudbot.util.formatting import ireplace

correction_re = re.compile(r"^[sS]/(.*/.*(?:/[igx]{,4})?)\S*$")


@hook.regex(correction_re)
def correction(match, conn, chan, message):
    """
    :type match: re.__Match
    :type conn: cloudbot.client.Client
    :type chan: str
    """
    groups = [b.replace("\/", "/") for b in re.split(r"(?<!\\)/", match.groups()[0])]
    find_regex = groups[0]
    replace = groups[1]

    for item in conn.history[chan].__reversed__():
        print(conn.history)
        nick, timestamp, msg = item
        if correction_re.match(msg):
            # don't correct corrections, it gets really confusing
            continue
        try:
            if re.search(find_regex, msg) is not None:
                #Remove if there
                if "\x01ACTION" in msg:
                    msg = msg.replace("\x01ACTION", "").replace("\x01", "")

                #Send bolded correction
                mod_msg = re.sub(find_regex, "\x02" + replace + "\x02", msg) #ireplace(msg, find_regex, "\x02" + replace + "\x02")
                message("Correction, <{}> {}".format(nick, mod_msg))

                #Add correction to the history
                msg = re.sub(find_regex, replace, msg)
                conn.history[chan].append((nick, timestamp, msg))
                return
            else:
                continue
        except IndexError:
            #There was an invalid backreference in the replace string. Treat as if no matches were found.
            continue
