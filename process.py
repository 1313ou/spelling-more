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
    esc = re.sub(r'\'tis\b', f'{APOS_SUB}tis', esc)
    esc = re.sub(r'o\'clock\b', f'o{APOS_SUB}clock', esc)
    esc = re.sub(r's\'\s', f's{APOS_SUB}', esc)  # plural genitive
    return esc


def uneven(input_text, c):
    collected = [m.start() for m in re.finditer(rf'{c}', input_text)]
    if len(collected) % 2 != 0:
        return collected[-1]
    else:
        return None


def unclosed(input_text, left, right):
    pat = rf'[{left}{right}]'
    # Find all parentheses in the text
    parentheses = [m.group() for m in re.finditer(pat, input_text)]

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
                return input_text.index(paren)

    # If stack is not empty, there are unclosed opening parentheses
    if stack:
        return input_text.rindex(left)
    else:
        return None


def find(input_text, what):
    if input_text.find(what) != -1:
        return True
    return None


def search(input_text, what):
    if re.search(fr"{what}", input_text):
        return True
    return None


#  C A L L A B L E

def find_unclosed_parentheses(input_text):
    return unclosed(input_text, '(', ')')


def find_unclosed_wn_quotes(input_text):
    return unclosed(input_text, '`', '\'')


def find_2_hyphens(input_text):
    return find(input_text, '--')


def search_2_hyphens(input_text):
    return search(input_text, '--')


def set_emdash_if_has_2_hyphens(input_text):
    r = r'\s*--\s*'
    s = " —— "
    if re.search(r, input_text):
        return re.sub(r, s, input_text)
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


def find_uneven_double_quotes(input_text):
    return uneven(input_text, '"')


def find_uneven_single_quotes(input_text):
    return uneven(input_text, '\'')


def set_apostrophe_escape(input_text):
    esc = escape_apostrophe(input_text)
    return f"{esc}" if esc != input_text else None


def find_unclosed_wn_quotes_excluding_apostrophe(input_text):
    esc = escape_apostrophe(input_text)
    return find_unclosed_wn_quotes(esc)


def with_semicolon_after_space(input_text):
    return search(input_text, r' ;')


def find_double_quotes(input_text):
    pattern = r'"'
    match = re.search(pattern, input_text)
    if match:
        return match.group()
    else:
        return None


def find_backtick(input_text):
    pattern = r'`'
    match = re.search(pattern, input_text)
    if match:
        return match.group()
    else:
        return None


def find_ie(input_text):
    pattern = (r'\bie\b')
    match = re.search(pattern, input_text)
    if match:
        return match.group()
    else:
        return None


def default_process(input_text):
    pattern = (r'\bie\b')
    match = re.search(pattern, input_text)
    if match:
        return match.group()
    else:
        return None
