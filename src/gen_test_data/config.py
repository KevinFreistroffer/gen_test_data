from __future__ import annotations

from dataclasses import dataclass
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
    OUTPUT_SUBDIR_IN_TARGET_REPO: str | None = None  # e.g., "testdata"

    # Map fully-qualified model name -> filename (without env prefix or extension)
    FILENAME_OVERRIDES: Dict[str, str] = FILENAME_OVERRIDES

    # Set of fully-qualified model names to exclude
    EXCLUDE_MODELS: Set[str] = EXCLUDE_MODELS


# Default settings reference the top-level configuration
DEFAULT_SETTINGS = Settings()
