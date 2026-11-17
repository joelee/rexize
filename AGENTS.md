# AGENTS.md

Python 3.12+ CLI tool (`rexize`) for bulk resizing/converting images recursively. Poetry-managed, published to PyPI. Pillow is the only runtime dependency.

## Commands

```bash
poetry install                                          # setup
poetry run pytest                                       # all tests (run from repo root)
poetry run pytest tests/test_file_iterator.py::test_file_iterator   # single test
poetry run pytest --cov=src --cov-report=term-missing tests/        # what CI runs; fails under 80% coverage
pre-commit run --all-files                             # mirrors CI: black, flake8, isort, poetry check
bin/rexize <args>                                       # run CLI locally (poetry run python src/main.py)
```

- Tests must run from the repo root: fixtures use relative paths (`tests/data/...`).
- Python 3.12 is the floor (`python = "^3.12"`) and CI tests 3.12 to 3.14; local development defaults to 3.14 (`.python-version`).

## Architecture

- The package is literally named `src`, and modules import each other **flat**, not `src.`-prefixed (`from cli import CLI`, `from image import ImageFormat`). `src/main.py` does a `sys.path.append` hack; tests get flat imports via `pythonpath = ["src"]` in `pyproject.toml`. Follow this convention for any new module in `src/`.
- Entry point: `rexize = src.main:main` (`pyproject.toml`); `bin/rexize.py` is a symlink to `src/main.py`.
- Flow in `src/main.py`: `CLI` (arg parse/validate) → `FileIterator` (recursive walk + extension filter) → `ImageManipulator` (Pillow resize/convert) → `get_output_file` (mirrors input tree under output dir, rewrites extension, maps `jpeg` → `jpg`).
- Supported input extensions are hardcoded in `src/main.py`: jpg, jpeg, png, webp, gif, tiff, bmp.
- `FileIterator.__init__` accepts either a `CLI` instance or a folder path string.
- Exit codes: 55 = invalid args, 1 = runtime error.
- `DEV_MODE` env var enables debug output in `CLI`.

## Style

- black line length 88; flake8 max-line-length 99 and ignores E203; isort uses the black profile. Configs: `pyproject.toml`, `.flake8`.

## Repo layout contracts

- Branches: `master` (default) and `development`; CI runs on PRs and pushes to both.
