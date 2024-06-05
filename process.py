import re


def find_unclosed_quotes_regex(text):
    pattern = r'"[^"]*$'
    match = re.search(pattern, text)
    if match:
        return True, match.group()
    else:
        return False, None


def find_uneven_quotes(text):
    # Find all quotes in the text
    quotes = [m.start() for m in re.finditer(r'"', text)]

    # If the number of quotes is odd, there is an unclosed quote
    if len(quotes) % 2 != 0:
        return True, quotes[-1]
    else:
        return False, None


def find_unclosed_parentheses(text):
    return find_unclosed(text, '`', '\'')


def find_unclosed_wn_quotes(text):
    return find_unclosed(text, '`', '\'')


def find_unclosed(text, left, right):
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
                return True, text.index(paren)

    # If stack is not empty, there are unclosed opening parentheses
    if stack:
        return True, text.rindex(left)
    else:
        return False, None


def has_2_hyphens_find(input_text):
    if input_text.find('--') != -1:
        return True
    return None


def has_2_hyphens(input_text):
    if re.search(r"--", input_text):
        return True
    return None


def emdash_if_has_2_hyphens_after_nonspace(input_text):
    if re.search(r"\S--", input_text):
        return re.sub(r"\s*--\s*", " —— ", input_text)
    return None


def etcdot(input_text):
    r = r"\betc[^.]"
    s = "@@@"
    if re.search(r, input_text):
        return re.sub(r, s, input_text)
    return None


def uneven_quotes(input_text):
    found, where = find_uneven_quotes(input_text)
    if found:
        return f" <{where}>"
    return None


def unclosed_parentheses(input_text):
    found, where = find_unclosed_parentheses(input_text)
    if found:
        return f" <{where}>"
    return None


def unclosed_wordnet_quotes(input_text):
    found, where = find_unclosed_wn_quotes(input_text)
    if found:
        return f" <{where}>"
    return None

r = '###'


def unescape_apostrophe(input_text):
    return re.sub(rf'{r}', r'\'', input_text)


def escape_apostrophe(input_text):
    esc = input_text
    esc = re.sub(r'(\S)\'s\b', f'\\1{r}s', esc)
    esc = re.sub(r'(\S)\'re\b', f'\\1{r}re', esc)
    esc = re.sub(r'(\S)\'ve\b', f'\\1{r}ve', esc)
    esc = re.sub(r'(\S)\'d\b', f'\\1{r}d', esc)
    esc = re.sub(r'(\S)\'ll\b', f'\\1{r}ll', esc)
    esc = re.sub(r'(\S)\'m\b', f'\\1{r}m', esc)
    esc = re.sub(r'n\'t\b', f'n{r}t', esc)
    return esc


def process_apostrophe(input_text):
    esc = escape_apostrophe(input_text)
    return f" -> {esc}" if esc != input_text else None


def process(input_text):
    esc = escape_apostrophe(input_text)
    found, where = find_unclosed_wn_quotes(esc)
    if found:
        return f" <{where}>"
    return None

"""
    re.match is anchored at the start ^pattern
        Ensures the string begins with the pattern
    re.fullmatch is anchored at the start and end of the pattern ^pattern$
        Ensures the full string matches the pattern (can be especially useful with alternations as described here)
    re.search is not anchored pattern
        Ensures the string contains the pattern
"""
