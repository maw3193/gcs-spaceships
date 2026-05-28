"""
GCS Script Inliner Config

Types and code for configuring GCS Script Inliner
"""
from pathlib import Path
from pydantic import BaseModel, Field, FilePath, DirectoryPath
from pydantic_yaml import parse_yaml_file_as

class Config(BaseModel):
    """
    GCS Script Inliner Config

    Attributes:
        javascript_sources: A list of javascript file paths, or paths to directories that contain javascript files
        libraries: A list of paths to directories that contain gcs files that should have javascript inlined
    """
    javascript_sources: list[FilePath | DirectoryPath] = Field(min_length=1)
    libraries: list[FilePath | DirectoryPath] = Field(min_length=1)

def load_config(config_file: Path) -> Config:
    return parse_yaml_file_as(Config, config_file)

