import random
import string


def rand_str(limit=6, include_lower=False, include_upper=True, include_digit=False):
    """Generate a random string of fixed length """

    letters = ""

    if include_lower:
        letters += string.ascii_lowercase

    if include_upper:
        letters += string.ascii_uppercase

    if include_digit:
        letters += string.digits

    return ''.join(random.choice(letters) for i in range(limit))


def link_to(path):
    return "http://127.0.0.1:8000" + path

def format_price(price):
    return "{} BDT".format(price)