import re


def slugify(string):
    """
    Slugify strings
    """
    string = string.lower()
    return re.sub(r'\W+', '-', string)
