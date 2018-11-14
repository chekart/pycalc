from collections import namedtuple

from lexer.scanner import Scanner


Token = namedtuple('Token', ('token_type', 'value'))


def tokenize(text):
    """
    Convert expression string to the list of tokens

    >>> list(map(tuple, tokenize('1')))
    [('NUM', 1)]
    >>> list(map(tuple, tokenize('1 +2')))
    [('NUM', 1), ('OP', '+'), ('NUM', 2)]
    >>> list(map(tuple, tokenize('0 || 2')))
    [('NUM', 0), ('OP', '||'), ('NUM', 2)]
    >>> tokenize('abc')
    Traceback (most recent call last):
        ...
    Exception: Unknown token a
    """
    scanner = Scanner(text)
    tokens = []

    # start scanning from whitespace
    do_scan = scan_space
    while do_scan:
        do_scan = do_scan(scanner, tokens)

    return tokens


def scan_space(scanner, tokens):
    """
    Ignore whitespace symbols
    Prepare to scan any token after
    """
    scanner.read_until(' \t')
    scanner.ignore()
    return scan_any


def scan_number(scanner, tokens):
    """
    Scan number until other symbol is found
    """
    scanner.read_until('1234567890.eE')
    # let's check if it's exponential form
    # tuple form for - and + since peek could return None
    if scanner.prev() in 'eE' and scanner.peek() in ('-', '+'):
        scanner.read()  # accepting -+ of exponential part
        scanner.read_until('1234567890')
    value_str = scanner.extract()
    value = None

    # try coerce to the needed format, order is important
    for coerce in (int, float):
        try:
            value = coerce(value_str)
            break
        except ValueError:
            pass

    # failed to convert, bad number format
    if value is None:
        raise Exception('Unknown token {}'.format(value))

    token = Token('NUM', value)
    tokens.append(token)
    return scan_space


def scan_logical(scanner, tokens):
    """Scan C-like logical operator && or ||"""
    prev = scanner.prev()
    # compare current symbol to previous one, since they are the same
    if scanner.read() == prev:
        tokens.append(Token('OP', scanner.extract()))
        return scan_space
    # &| is not a known logical token
    raise Exception('Unknown token {}'.format(scanner.extract()))


def scan_any(scanner, tokens):
    """Try to scan any possible input symbol"""
    ch = scanner.read()
    if ch is None:
        # end of the expression source
        return None

    if ch in '+-*/':
        tokens.append(Token('OP', scanner.extract()))
        return scan_space

    if ch in '&|':
        return scan_logical

    if ch in '1234567890':
        return scan_number

    if ch in '()':
        tokens.append(Token(ch, scanner.extract()))
        return scan_space

    raise Exception('Unknown token {}'.format(ch))
