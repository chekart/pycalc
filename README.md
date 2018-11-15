[![Build Status](https://travis-ci.org/chekart/pycalc.svg?branch=dev)](https://travis-ci.org/chekart/pycalc)

# pycalc

Parsing mathematical expressions in Python
Supported operations:
- mathematical + - * /
- logical && ||
- brackets ()
- negation

#### Algorythms used

Custom written tokenize logic based on [Rob Pike's](https://github.com/robpike) talk "Lexical Scanning in Go"

Shunting yard extended with negate operation used for expression evaluation

#### Notes

For simplicity all custom exceptions are of base class Exception

For simplicity token type is string
