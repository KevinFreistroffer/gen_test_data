# gen_test_data

Generate JSON test data from Pydantic models and push artifacts to a separate repository.

## How it works

- Discovers all `pydantic.BaseModel` classes under the `schemas` package
- Generates example JSON for each model
- Writes three files per model: `DEV_<name>.json`, `QA_<name>.json`, `PROD_<name>.json`
- Filenames default to the model class name; you can override via `src/gen_test_data/config.py`
- A GitHub Action runs on push, regenerates outputs, and pushes to a separate repo

## Quick start (local)

1. Python 3.11+
2. Install deps:
   ```bash
   python -m venv .venv && . .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Create your models under `src/schemas/`:
   - e.g., `src/schemas/user.py` with `class User(BaseModel): ...`
4. Run generator:
   - Bash/Mac/Linux:
     ```bash
     PYTHONPATH=src python -m gen_test_data
     ```
   - Windows PowerShell:
     ```powershell
     $env:PYTHONPATH = "src"; python -m gen_test_data
     ```
     Outputs go to `output/`

## Filename overrides

Edit `src/gen_test_data/config.py`:

```python
FILENAME_OVERRIDES = {
    # "schemas.user.User": "users",  # results in DEV_users.json, ...
}
```

Use fully-qualified name: `"<package>.<module>.<ClassName>"`.

## Pushing to another repository (CI)

The workflow `.github/workflows/generate-and-push.yml` expects secrets:

- `PUSH_TOKEN`: PAT with repo access to the target repository
- `TARGET_REPO`: e.g., `your-org/testdata-repo`
- `TARGET_BRANCH` (optional): defaults to `main`
- `OUTPUT_SUBDIR` (optional): subdirectory within the target repo

On push, the action:

- Checks out this repo and the target repo
- Generates outputs
- Copies `output/` into the target repo root (or the specified `OUTPUT_SUBDIR`)
- Commits and pushes only if there are changes

## Configuration

See `src/gen_test_data/config.py` for:

- `SCHEMAS_PACKAGE`: where models live (default `schemas`)
- `OUTPUT_DIR`: where to write files (default `output`)
- `OUTPUT_SUBDIR_IN_TARGET_REPO`: optional subdir inside the target repo
- `FILENAME_OVERRIDES` and `EXCLUDE_MODELS`

## Notes

- Uses `polyfactory` + `faker` to synthesize realistic values
- Handles nested models and collections
- Skips abstract or generic models

test
