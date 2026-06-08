"""
Inlining code

The top-level code for performing inlining
"""
import json
import subprocess

from .config import Config
from .gcs import EquipmentList, gcs_library_files
from .javascript import collect_source_javascript, inline_javascript, javascript_files

def inline(config: Config) -> None:
    # Inlining takes two big things and munges them together:
    # 1. Collecting all the javascript from config.javascript_sources.
    # 2. Inserting functions (and constants I guess) from javascript sources into gcs.
    # first, let's start small, I have minimal gcs and javascript to prove it works.
    js_files = list(javascript_files(config.javascript_sources))
    for file_path in js_files:
        # I haven't decided how to handle output yet
        src_js = collect_source_javascript(file_path.read_text())

    gcs_files = list(gcs_library_files(config.libraries))
    for file_path in gcs_files:
        equipment = EquipmentList.model_validate_json(file_path.read_text())
        equipment.mutate_scripts(inline_javascript)
        file_path.write_text(equipment.model_dump_json())

    cmdline = [config.gcs_command, "-convert"]
    cmdline.extend(f.as_posix() for f in gcs_files)
    subprocess.run(cmdline)
    
