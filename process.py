import re

#  H E L P E R S

APOS_SUB = '###'


def unescape_apostrophe(input_text):
    return re.sub(rf'{APOS_SUB}', r'\'', input_text)


# this does not handle Socrates'.others' genitives
def escape_apostrophe(input_text):
    esc = input_text
    esc = re.sub(r'(\S)\'s\b', f'\\1{APOS_SUB}s', esc)
    esc = re.sub(r'(\S)\'re\b', f'\\1{APOS_SUB}re', esc)
    esc = re.sub(r'(\S)\'ve\b', f'\\1{APOS_SUB}ve', esc)
    esc = re.sub(r'(\S)\'d\b', f'\\1{APOS_SUB}d', esc)
    esc = re.sub(r'(\S)\'ll\b', f'\\1{APOS_SUB}ll', esc)
    esc = re.sub(r'(\S)\'m\b', f'\\1{APOS_SUB}m', esc)
    esc = re.sub(r'n\'t\b', f'n{APOS_SUB}t', esc)
    return esc


def unclosed(text, left, right):
    pat = rf'[{left}{right}]'
    # Find all parentheses in the text
    parentheses = [m.group() for m in re.finditer(pat, text)]

    # Stack to track unclosed parentheses
    stack = []
    for paren in parentheses:
        if paren == left:
            stack.append(paren)
        elif paren == right:
            if stack and stack[-1] == left:
                stack.pop()
            else:
                # An unmatched closing parenthesis found
                return text.index(paren)

    # If stack is not empty, there are unclosed opening parentheses
    if stack:
        return text.rindex(left)
    else:
        return None


def find_unclosed_parentheses(text):
    return unclosed(text, '`', '\'')


def find_unclosed_wn_quotes(text):
    return unclosed(text, '`', '\'')


#  C A L L A B L E

def find_2_hyphens_find(input_text):
    if input_text.find('--') != -1:
        return True
    return None


def find_2_hyphens(input_text):
    if re.search(r"--", input_text):
        return True
    return None


def set_emdash_if_has_2_hyphens_after_nonspace(input_text):
    if re.search(r"\S--", input_text):
        return re.sub(r"\s*--\s*", " —— ", input_text)
    return None


def set_etcdot(input_text):
    r = r'\betc([^\.a-z])'
    s = "etc.\\1"
    if re.search(r, input_text):
        return re.sub(r, s, input_text)
    return None


def set_egdot(input_text):
    r = r'\beg\b'
    s = "e.g."
    if re.search(r, input_text):
        return re.sub(r, s, input_text)
    return None


def set_apostrophe_escape(input_text):
    esc = escape_apostrophe(input_text)
    return f" -> {esc}" if esc != input_text else None


def find_unclosed_quotes_regex(text):
    pattern = r'"[^"]*$'
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


def find_uneven_quotes(text):
    # Find all quotes in the text
    quotes = [m.start() for m in re.finditer(r'"', text)]

    # If the number of quotes is odd, there is an unclosed quote
    if len(quotes) % 2 != 0:
        return quotes[-1]
    else:
        return None


def find_unclosed_wn_quotes_excluding_apostrophe(input_text):
    esc = escape_apostrophe(input_text)
    found, where = find_unclosed_wn_quotes(esc)
    if found:
        return f" <{where}>"
    return None


def default_process(input_text):
    #pattern = r';.*;'
    pattern = r' ;'
    match = re.search(pattern, input_text)
    if match:
        return match.group()
    else:
        return None
