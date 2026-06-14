"""
Javascript code

The central point for javascript-based operations
"""
import json
from collections.abc import Sequence
from itertools import chain
from pathlib import Path
import sys
from typing import Generator

from tree_sitter import Language, Node, Parser, Tree
import tree_sitter_javascript as tsjs

JS_LANGUAGE = Language(tsjs.language())

# any identifiers used directly inside one of these is being declared instead of being used
DECLARATION_TYPES = (
    "variable_declarator", # var foo = 1
    "function_declaration", # function foo(...)
    "formal_parameters", # function ...(foo)
    "assignment_pattern" # function ...(foo=1)
)


JAVASCRIPT_BUILTINS = frozenset((
    "globalThis",
    "Infinity",
    "NaN",
    "undefined",
    "eval",
    "isFinite",
    "isNaN",
    "parseFloat",
    "parseInt",
    "decodeURI",
    "decodeURIComponent",
    "encodeURI",
    "encodeURIComponent",
    "escape",
    "unescape",
    "Object",
    "Function",
    "Boolean",
    "Symbol",
    "Error",
    "AggregateError",
    "EvalError",
    "RangeError",
    "ReferenceError",
    "SuppressedError",
    "SyntaxError",
    "TypeError",
    "URIError",
    "InternalError",
    "Number",
    "BigInt",
    "Math",
    "Date",
    "Temporal",
    "String",
    "RegExp",
    "Array",
    "TypedArray",
    "Int8Array",
    "Uint8Array",
    "Uint8ClampedArray",
    "Int16Array",
    "Uint16Array",
    "Int32Array",
    "Uint32Array",
    "BigInt64Array",
    "BigUint64Array",
    "Float16Array",
    "Float32Array",
    "Float64Array",
    "Map",
    "Set",
    "WeakMap",
    "WeakSet",
    "ArrayBuffer",
    "SharedArrayBuffer",
    "DataView",
    "Atomics",
    "JSON",
    "WeakRef",
    "FinalizationRegistry",
    "Iterator",
    "AsyncIterator",
    "Promise",
    "GeneratorFunction",
    "AsyncGeneratorFunction",
    "Generator",
    "AsyncGenerator",
    "AsyncFunction",
    "DisposableStack",
    "AsyncDisposableStack",
    "Reflect",
    "Proxy",
    "Intl",
    "Intl.Collator",
    "Intl.DateTimeFormat",
    "Intl.DisplayNames",
    "Intl.DurationFormat",
    "Intl.ListFormat",
    "Intl.Locale",
    "Intl.NumberFormat",
    "Intl.PluralRules",
    "Intl.RelativeTimeFormat",
    "Intl.Segmenter",
))

class SourceJavascriptItem(object):
    node: Node
    missing: Sequence[str] # names of identifiers used but not defined in this node

    def __init__(self, node, missing):
        self.node = node
        self.missing = missing

    def __str__(self):
        return f"(node: {self.node.type}, missing: {self.missing})"

    def __repr__(self):
        return self.__str__()


type SourceJavascriptDict = dict[str, SourceJavascriptItem]


def is_js_file(path: Path) -> bool:
    return path.is_file() and path.suffix in (".js")


def javascript_files(paths: list[Path]):
    for js_path in paths:
        if is_js_file(js_path):
            yield js_path
            continue

        for dir_path, _, files in js_path.walk():
            for file in files:
                file_path = dir_path / file
                if is_js_file(file_path):
                    yield file_path


def traverse_tree(node: Node) -> Generator[Node, None, None]:
    yield node
    for child in node.children:
        yield from traverse_tree(child)


def find_declared_identifiers(root: Node) -> list[Node]:
    # any identifier inside a variable_declarator or function_declaration.
    return [node for node in traverse_tree(root) if node.type == "identifier" and node.parent.type in DECLARATION_TYPES]


def find_used_identifiers(root: Node):
    # any identifier that's in something other than a variable_declarator or function_declarator.
    return [node for node in traverse_tree(root) if node.type == "identifier" and node.parent.type not in DECLARATION_TYPES]


def find_identifiers(root: Node):
    return [node for node in traverse_tree(root) if node.type == "identifier"]


def find_missing_identifiers(root: Node, builtins: Sequence[str]) -> set[str]:
    return (
        set(i.text.decode("utf-8") for i in find_used_identifiers(root))
        - set(i.text.decode("utf-8") for i in find_declared_identifiers(root))
        - set(builtins)
    )


def get_missing_identifiers(text: str, builtins: Sequence[str]) -> set[str]:
    """Parse the text as a javascript program, listing the identifiers that are used but not declared in the text"""
    parser = Parser(JS_LANGUAGE)
    tree = parser.parse(bytes(text, "utf8"))
    program = tree.root_node
    return find_missing_identifiers(program, builtins)


def display_node(node):
    return str(node)


def collect_source_javascript(text: str, builtins: Sequence[str]) -> SourceJavascriptDict:
    """Parse the text as a javascript program, providing top-level identifiers of the program, alongside lists of identifiers used outside of those declarations"""
    parser = Parser(JS_LANGUAGE)
    tree = parser.parse(bytes(text, "utf8"))
    program = tree.root_node
    print("*** SOURCE AST", program)
    sources = {}
    for child in program.children:
        if child.type == "variable_declaration":
            # child.children[0] is "let", "var" or "const"
            # child.children[1] should be a variable declarator
            assert child.children[1].type == "variable_declarator"
            # assuming it's not declaring multiple at once
            identifier_name = child.children[1].children[0].text.decode("utf-8")
            missing = find_missing_identifiers(child, builtins)
            sources[identifier_name] = SourceJavascriptItem(child, missing)
        elif child.type == "function_declaration":
            identifier_name = child.child_by_field_name("name").text.decode("utf-8")
            missing = find_missing_identifiers(child, builtins)
            sources[identifier_name] = SourceJavascriptItem(child, missing)
        else:
            sys.stderr.write(f"Unexpected code! what am I supposed to do with {child.text.decode('utf-8')}\n")

    return sources


def total_used_identifiers(missing: Sequence[str], extra_sources: SourceJavascriptDict) -> Sequence[str]:
    """Identifiers used by `missing` or `extra_sources`"""
    used = set(missing)
    for source in extra_sources.values():
        used |= source.missing
    return used


def unsatisfiable_identifiers(missing: Sequence[str], extra_sources: SourceJavascriptDict) -> Sequence[str]:
    """Identifiers used by `missing` or `extra_sources` that aren't also provided by `extra_sources`"""
    return set(total_used_identifiers) - set(extra_sources.keys())


def satisfy_missing_identifiers(missing: Sequence[str], extra_sources: SourceJavascriptDict, builtins: Sequence[str]) -> str:
    """Generate text of javascript code that provides every identifier requested in `missing` using identifiers provided by `extra_sources`. If a declaration from extra_sources requires extra identifiers, add those too."""
    missing = list(missing)
    keys = []
    while missing:
        new_miss = missing.pop()
        if new_miss in keys:
            # already satisfied
            continue
        if new_miss not in extra_sources and new_miss not in builtins:
            sys.stderr.write(f"Can't satisfy {new_miss}\n")
            continue
        source = extra_sources[new_miss]
        missing.extend(source.missing)
        keys.append(new_miss)
    return "\n".join(extra_sources[key].node.text.decode("utf-8") for key in keys)

def strip_library_identifiers(text: str, library: SourceJavascriptDict) -> str:
    """Generate text of javascript code that removes all top-level declarations that are also provided by `library`. This is intended to be used to remove variables and functions provided by `library`, before adding more recent versions."""
    parser = Parser(JS_LANGUAGE)
    tree = parser.parse(bytes(text, "utf8"))
    program = tree.root_node
    keep_text = []
    for node in program.children:
        if node.type == "variable_declaration":
            name = node.children[1].children[0].text.decode("utf-8")
            if name in library:
                continue
        elif node.type == "function_declaration":
            name = node.child_by_field_name("name").text.decode("utf-8")
            if name in library:
                continue
        keep_text.append(node.text.decode("utf-8"))

    return "\n".join(keep_text)
