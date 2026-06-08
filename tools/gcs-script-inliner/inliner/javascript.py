"""
Javascript code

The central point for javascript-based operations
"""
import json
from collections.abc import Sequence
from itertools import chain
from pydantic import BaseModel
from slimit import minify
from slimit.ast import Catch, DotAccessor, FuncBase, Identifier, Node, Program, VarDecl
import slimit.parser


class SourceJavascriptItem(BaseModel):
    node: Node
    missing: list[Node]


# based on slimit.ast's declaration of an identifier as _mangle_candidate
def find_declared_identifiers(node):
    if isinstance(node, VarDecl):
        yield node.identifier
    elif isinstance(node, Catch):
        yield node.identifier
    elif isinstance(node, FuncBase):
        yield node.identifier
        for param in node.parameters:
            yield param
    else:
        for child in node.children():
            yield from find_declared_identifiers(child)


# any instance of Identifier that's not declaring one is using one
# dot accessors of foo.bar we only care about the foo.
def find_used_identifiers(node):
    if isinstance(node, Identifier):
        yield node
    elif isinstance(node, VarDecl):
        yield from find_used_identifiers(node.initializer)
    elif isinstance(node, Catch):
        for element in node.elements:
            yield from find_used_identifiers(element)
    elif isinstance(node, FuncBase):
        for element in node.elements:
            yield from find_used_identifiers(element)
    elif isinstance(node, DotAccessor):
        yield node.node
    else:
        for child in node.children():
            yield from find_used_identifiers(child)


def find_identifiers(node):
    return chain(find_declared_identifiers(node), find_used_identifiers(node))


def find_missing_identifiers(node) -> set[str]:
    return set(i.value for i in find_used_identifiers(node)) - set(i.value for i in find_declared_identifiers(node))


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
    #print(list(find_identifiers(program)))
    identifiers = list((i.value, getattr(i, "_mangle_candidate", None)) for i in find_identifiers(program))
    print(identifiers)
    print(
        "Declared:", [i.value for i in find_declared_identifiers(program)],
        "Used:", [i.value for i in find_used_identifiers(program)],
        "Missing:", find_missing_identifiers(program),
    )
    #print("***AST***")
    #print(json.dumps(display_node(program), indent=2))
    print("***")
    return text
