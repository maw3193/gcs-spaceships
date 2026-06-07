"""
Inlining code

The top-level code for performing inlining
"""
import json
import subprocess

from .config import Config
from .gcs import EquipmentList, gcs_library_files
from .javascript import inline_javascript

def inline(config: Config) -> None:
    # Inlining takes two big things and munges them together:
    # 1. Collecting all the javascript from config.javascript_sources.
    # 2. Inserting functions (and constants I guess) from javascript sources into gcs.
    # first, let's start small, I have minimal gcs and javascript to prove it works.
    files = list(gcs_library_files(config.libraries))
    for file_path in files:
        equipment = EquipmentList.model_validate_json(file_path.read_text())
        equipment.mutate_scripts(inline_javascript)
        file_path.write_text(equipment.model_dump_json())

    cmdline = [config.gcs_command, "-convert"]
    cmdline.extend(f.as_posix() for f in files)
    subprocess.run(cmdline)
    
