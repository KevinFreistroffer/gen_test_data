from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Set


# Edit these mappings to customize behavior
FILENAME_OVERRIDES: Dict[str, str] = {
    # Example: "schemas.user.User": "users",
}
EXCLUDE_MODELS: Set[str] = set()


@dataclass(frozen=True)
class Settings:
    # Package or dotted path where your Pydantic models live
    SCHEMAS_PACKAGE: str = "schemas"

    # Local output directory for generated files
    OUTPUT_DIR: str = "output"

    # Optional subdirectory inside the target repo where files should be copied by CI
    OUTPUT_SUBDIR_IN_TARGET_REPO: str | None ="dev"

    # Map fully-qualified model name -> filename (without env prefix or extension)
    FILENAME_OVERRIDES: Dict[str, str] = field(default_factory=dict)

    # Set of fully-qualified model names to exclude
    EXCLUDE_MODELS: Set[str] = field(default_factory=set)


# Default settings reference the top-level configuration
DEFAULT_SETTINGS = Settings(
    FILENAME_OVERRIDES=FILENAME_OVERRIDES,
    EXCLUDE_MODELS=EXCLUDE_MODELS,
)
