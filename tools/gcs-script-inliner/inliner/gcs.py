"""
GCS

Code for handling the GCS side of inlining
"""

from collections.abc import Callable
from pathlib import Path
from pydantic import BaseModel, ConfigDict
import re
from typing import Any, Optional, Self, TypedDict


type ScriptMutator = Callable[[str], str]


GCS_FILE_EXTENSIONS = (".eqp")


def is_gcs_file(path: Path) -> bool:
    return path.is_file() and path.suffix in GCS_FILE_EXTENSIONS


def gcs_library_files(paths: list[Path]):
    for library_path in paths:
        if is_gcs_file(library_path):
            yield library_path
            continue

        for dir_path, _, files in library_path.walk():
            for file in files:
                file_path = dir_path / file
                if is_gcs_file(file_path):
                    yield file_path


def mutate_scripted_string(s: str, mutator: ScriptMutator) -> str:
    def mutate_match(match):
        return "<script>" + mutator(match.group(1)) + "</script>"
    script_expr = r"<script>(.*?)</script>"

    new = re.sub(script_expr, mutate_match, s, flags=re.DOTALL)
    return new


class EquipmentModifier(BaseModel):

    model_config = ConfigDict(extra="allow")


class PrereqList(BaseModel):

    model_config = ConfigDict(extra="allow")


class Weapon(BaseModel):
    
    model_config = ConfigDict(extra="allow")


class EquipmentItem(BaseModel):
    local_notes: Optional[str] = None  # may contain scripts in tags
    base_value: Optional[str] = None  # is a script or literal
    base_weight: Optional[str] = None  # is a script or literal
    prereqs: Optional[PrereqList] = None  # prereqs may contain scripts
    weapons: Optional[list[Weapon]] = None  # weapons may contain scripts
    modifiers: list[EquipmentModifier] = [] # modifiers may contain scripts
    children: Optional[list[Self]] = None 

    model_config = ConfigDict(extra="allow")

    def mutate_scripts(self, mutator: ScriptMutator):
        if self.base_value:
            self.base_value = mutator(self.base_value)
        if self.base_weight:
            self.base_weight = mutator(self.base_weight)
        if self.local_notes:
            self.local_notes = mutate_scripted_string(self.local_notes, mutator)
        if self.children:
            for child in self.children:
                child.mutate_scripts(mutator)


class EquipmentList(BaseModel):
    version: int # assert it matches the version I expect
    rows: list[EquipmentItem]

    model_config = ConfigDict(extra="allow")

    def mutate_scripts(self, mutator: ScriptMutator):
        for row in self.rows:
            row.mutate_scripts(mutator)
