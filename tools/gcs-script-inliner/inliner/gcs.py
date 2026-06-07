"""
GCS

Code for handling the GCS side of inlining
"""

import re
from typing import Any, Optional, Self, TypedDict
from collections.abc import Callable

type ScriptMutator = Callable[[str], str]

def mutate_scripted_string(s: str, mutator: ScriptMutator) -> str:
    def mutate_match(match):
        return mutator(match.group(0))
    script_expr = r"<script>(.*?)</script>"
    return re.sub(script_expr, mutate_match, s)

class EquipmentModifier(TypedDict, total=False):
    pass

class PrereqList(TypedDict, total=False):
    pass

class Weapon(TypedDict, total=False):
    pass

class EquipmentItem(TypedDict, total=False):
    local_notes: Optional[str] # may contain scripts in tags
    base_value: Optional[str] # is a script or literal
    base_weight: Optional[str] # is a script or literal
    prereqs: Optional[PrereqList] # prereqs may contain scripts
    weapons: Optional[list[Weapon]] # weapons may contain scripts
    modifiers: list[EquipmentModifier] = [] # modifiers may contain scripts
    children: Optional[list[Self]]

    def mutate_scripts(self, mutator: ScriptMutator):
        if self.base_value:
            self.base_value = mutator(self.base_value)
        if self.base_weight:
            self.base_weight = mutator(self.base_weight)
        if self.local_notes:
            self.local_notes = mutate_scripted_string(self.local_notes, mutator)

class EquipmentList(TypedDict, total=False):
    version: int # assert it matches the version I expect
    rows: list[EquipmentItem]

    def mutate_scripts(self, mutator: ScriptMutator):
        for row in rows:
            row.mutate_scripts(mutator)
