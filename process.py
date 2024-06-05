import re


def process1(input_text):
    if input_text.find('--') != -1:
        return True
    return None


def process2(input_text):
    if re.search(r"--", input_text):
        return True
    return None


def process(input_text):
    if re.search(r"\S--", input_text):
        return re.sub(r"\s*--\s*", " —— ", input_text)
    return None


"""
    re.match is anchored at the start ^pattern
        Ensures the string begins with the pattern
    re.fullmatch is anchored at the start and end of the pattern ^pattern$
        Ensures the full string matches the pattern (can be especially useful with alternations as described here)
    re.search is not anchored pattern
        Ensures the string contains the pattern
"""
