"""
Inlining code

The top-level code for performing inlining
"""
import json

from .config import Config
from .gcs import EquipmentList, gcs_library_files

def inline(config: Config) -> None:
    # Inlining takes two big things and munges them together:
    # 1. Collecting all the javascript from config.javascript_sources.
    # 2. Inserting functions (and constants I guess) from javascript sources into gcs.
    # first, let's start small, I have minimal gcs and javascript to prove it works.
    for file_path in gcs_library_files(config.libraries):
        equipment = EquipmentList.model_validate_json(file_path.read_text())
        equipment.mutate_scripts(str.upper)
        file_path.write_text(equipment.model_dump_json())

    # Ok, I have enough gcs processing to see how this'll work. I need to parse an manipulate gcs files.
    
