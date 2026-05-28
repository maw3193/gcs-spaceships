"""
GCS

Code for handling the GCS side of inlining
"""

# AAARGH! THERE'S TOO MUCH TO DESCRIBE THE WHOLE DATA MODEL IN PYTHON
# USE A TYPEDDICT SO IT'S ROUNDTRIPPABLE WITHOUT DESCRIBING EVERYTHING
from pydantic import BaseModel, PositiveInt
from typing import Any, Optional, Self

class EquipmentModifier(BaseModel):
    pass

class Features(BaseModel):
    pass

class PrereqList(BaseModel):
    pass

class EquipmentItem(BaseModel):
    id: str
    description: Optional[str]
    reference: Optional[str]
    reference_highlight: Optional[str]
    local_notes: Optional[str]
    tech_level: Optional[str]
    legality_class: Optional[str]
    tags: Optional[list[str]] = []
    base_value: Optional[str]
    base_weight: Optional[str]
    uses: Optional[int]
    max_uses: Optional[PositiveInt]
    prereqs: Optional[PrereqList]
    weapons: Optional[list[Weapon]] = []
    features: Optional[Features]
    ignore_weight_for_skills: bool = False
    vtt_notes: Optional[str]
    replacements: dict[str, str] = {}
    modifiers: list[EquipmentModifier] = []
    rated_strength: Optional[int]
    quantity: Optional[int]
    level: Optional[int]
    equipped: bool = False
    third_party: dict[str, Any] = {} # lol I've never seen this used
    children: Optional[list[Self]]

class EquipmentList(BaseModel):
    version: int
    rows: list[EquipmentItem]
