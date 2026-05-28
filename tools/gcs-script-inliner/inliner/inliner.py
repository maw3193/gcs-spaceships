"""
Inlining code

The top-level code for performing inlining
"""
from .config import Config

def inline(config: Config) -> None:
    # Inlining takes two big things and munges them together:
    # 1. Collecting all the javascript from config.javascript_sources.
    # 2. Inserting functions (and constants I guess) from javascript sources into gcs.
    # first, let's start small, I have minimal gcs and javascript to prove it works.
