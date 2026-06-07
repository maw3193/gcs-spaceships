"""
Javascript code

The central point for javascript-based operations
"""
import json
from collections.abc import Sequence
from slimit import minify
from slimit.ast import Identifier, Node, Program
import slimit.parser


def find_identifiers(node):
    if isinstance(node, Identifier):
        yield node

    for child in node.children():
        yield from find_identifiers(child)


def declared_identifiers(identifiers: Sequence[Identifier]) -> set[str]:
    return set(i.value for i in identifiers if getattr(i, "_mangle_candidate", False))


def used_identifiers(identifiers: Sequence[Identifier]) -> set[str]:
    return set(i.value for i in identifiers if not getattr(i, "_mangle_candidate", False))


def missing_identifiers(identifiers: Sequence[Identifier]) -> set[str]:
    identifiers = list(identifiers)
    return used_identifiers(identifiers) - declared_identifiers(identifiers)


def display_node(node):
    if not hasattr(node, "__dict__"):
        return node

    d = {}
    d["name"] = node.__class__.__name__
    for k, v in node.__dict__.items():
        if hasattr(v, "__dict__"):
            d[k] = display_node(v)
        elif isinstance(v, list):
            d[k] = [display_node(i) for i in v]
        else:
            d[k] = v
    return d


def inline_javascript(text: str) -> str:
    #print("***INPUT CODE***")
    #print(text)
    program = slimit.parser.Parser().parse(text)
    print("***PROGRAM***")
    print(program.to_ecma())
    print("***IDENTIFIERS**")
    identifiers = list(find_identifiers(program))
    print("Declared:", declared_identifiers(identifiers), "Used:", used_identifiers(identifiers), "Missing:", missing_identifiers(identifiers))
    #print("***AST***")
    #print(json.dumps(display_node(program), indent=2))
    print("***")
    return text
