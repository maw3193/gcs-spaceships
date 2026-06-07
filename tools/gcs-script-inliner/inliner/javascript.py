"""
Javascript code

The central point for javascript-based operations
"""
from slimit import minify
import slimit.parser


def inline_javascript(text: str) -> str:
    program = slimit.parser.Parser().parse(text)
    print(program.to_ecma())
    return text
