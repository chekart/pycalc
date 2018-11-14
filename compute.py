import operator

from lexer.tokenizer import Token, tokenize


OP_PRECEDENCE_LIST = [
    ('&&', '||'),
    ('+', '-'),
    ('*', '/'),
    ('neg',),
]


# Convert human readable precedence list into precedence map
OP_PRECEDENCE_MAP = {
    op: index for index, ops in enumerate(OP_PRECEDENCE_LIST) for op in ops
}


# Map operation tokens into actual operations
OP_MAP = {
    '*': operator.mul,
    '/': operator.truediv,
    '+': operator.add,
    '-': operator.sub,
    'neg': operator.neg,
    '&&': lambda l, r: l and r,
    '||': lambda l, r: l or r,
}


# Set of unary operations, to not scan for second operand
UNARY_OPS = {'neg'}


def compute(expression):
    """
    Compute mathematical expression presented as string

    >>> compute('12 + (1 + 5 * 6) - 7 + 3 * 2')
    42
    >>> compute('1 + 3 && 2 + 5 * 2')
    12
    >>> compute('0 || 1')
    1
    >>> compute('5')
    5
    >>> compute('-1 + (-2)')
    -3
    """
    tokens = tokenize(expression)
    return evaluate_tokens(tokens)


def _normalize_expression(tokens):
    """Yields corrected expression tokens, we need to split negate operation from binary minus operation"""
    prev = None
    for token in tokens:
        # Lets allow minus sign only at the beginning of the expression or after open bracket
        if (token.token_type == 'OP' and token.value == '-') and (prev is None or prev.token_type == '('):
            token = Token('OP', 'neg')

        yield token
        prev = token


def _to_rpn(tokens):
    """Convert tokens into Reverse Polish Notation using Shunting Yard algorithm"""
    rpn = []
    ops = []

    for token in _normalize_expression(tokens):
        if token.token_type == 'NUM':
            rpn.append(token)
        elif token.token_type == '(':
            ops.append(token)
        elif token.token_type == ')':
            try:
                while True:
                    last = ops.pop()
                    if last.token_type == '(':
                        break
                    rpn.append(last)
            except IndexError:
                raise Exception('Unmatched bracket')
        elif token.token_type == 'OP':
            while ops:
                last = ops[-1]
                if last.token_type == '(':
                    break
                if OP_PRECEDENCE_MAP[token.value] > OP_PRECEDENCE_MAP[last.value]:
                    break
                rpn.append(ops.pop())

            ops.append(token)

    while ops:
        last = ops.pop()
        if last.token_type == '(':
            raise Exception('Unmatched bracket')
        rpn.append(last)

    return rpn


def _evaluate(rpn):
    """Evaluate reverse polish notation in recursive manner, rpn is reversed iterator"""
    try:
        token = next(rpn)
    except StopIteration:
        raise Exception('Bad expression')

    if token.token_type == 'NUM':
        return token.value

    # the token is operator
    op = OP_MAP[token.value]
    right_operand = _evaluate(rpn)

    if token.value in UNARY_OPS:
        return op(right_operand)

    left_operand = _evaluate(rpn)
    return op(left_operand, right_operand)


def evaluate_tokens(tokens):
    rpn = _to_rpn(tokens)
    return _evaluate(iter(reversed(rpn)))
