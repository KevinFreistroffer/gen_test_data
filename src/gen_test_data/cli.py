from __future__ import annotations

import argparse
from pathlib import Path

from .config import DEFAULT_SETTINGS, Settings
from .generator import generate_and_write


def parse_args() -> Settings:
    parser = argparse.ArgumentParser(description="Generate JSON test data from Pydantic models.")
    parser.add_argument("--schemas", default=DEFAULT_SETTINGS.SCHEMAS_PACKAGE, help="Schemas package name")
    parser.add_argument("--out", default=DEFAULT_SETTINGS.OUTPUT_DIR, help="Output directory")
    parser.add_argument(
        "--subdir-in-target-repo",
        default=DEFAULT_SETTINGS.OUTPUT_SUBDIR_IN_TARGET_REPO,
        help="Optional subdir name to use in target repo (CI step)",
    )
    ns = parser.parse_args()
    return Settings(
        SCHEMAS_PACKAGE=ns.schemas,
        OUTPUT_DIR=ns.out,
        OUTPUT_SUBDIR_IN_TARGET_REPO=ns.subdir_in_target_repo,
        FILENAME_OVERRIDES=DEFAULT_SETTINGS.FILENAME_OVERRIDES,
        EXCLUDE_MODELS=DEFAULT_SETTINGS.EXCLUDE_MODELS,
    )


def main() -> int:
    settings = parse_args()
    outputs = generate_and_write(settings)
    if not outputs:
        print("No Pydantic models found. Ensure your models are under the 'schemas' package.")
        return 0
    out_root = Path(settings.OUTPUT_DIR).resolve()
    print(f"Wrote {len(outputs)} files to {out_root}")
    return 0

