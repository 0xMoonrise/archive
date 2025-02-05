import re

pattern = re.compile(r'\.(md|pdf)$')


def is_valid_file_ext(string):
    return bool(pattern.search(string))
