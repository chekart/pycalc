import sys

from compute import compute


def print_command_expression_result(expression):
    result = compute(expression)
    print(result)
    sys.stdout.flush()


def expression_loop():
    try:
        while True:
            expression = input('Expression: ')
            try:
                result = compute(expression)
            except Exception:
                print('Wrong expression')
            else:
                print('Result: {}'.format(result))
    except KeyboardInterrupt:
        print('\nBye!')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print_command_expression_result(sys.argv[1])
    else:
        expression_loop()
