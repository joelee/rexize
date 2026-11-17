# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`AGENTS.md` is the primary project guide (commands, flat-import convention, style, `docs/` report contracts, exit codes). Read it first; this file only adds what it doesn't cover.

## Commands

```bash
poetry install
poetry run pytest                                                 # run from repo root (fixtures use relative paths)
poetry run pytest tests/test_file_iterator.py::test_file_iterator # single test
poetry run pytest --cov=src --cov-report=term-missing tests/      # CI invocation, fails under 62%
pre-commit run --all-files                                        # black, flake8, isort, poetry check
bin/rexize -W 800 in_dir out_dir -f webp                          # run the CLI locally
```

## Architecture notes that span files

- `src/` is the package name but modules import each other flat (`from cli import CLI`). New modules must follow this; `main.py` appends its own directory to `sys.path` and pytest uses `pythonpath = ["src"]`.
- **Size values are `ImageSizeUnit` objects** (`image.py`), not ints. `CLI._argparser` wraps `--width`, `--height` and `--max-size` into `ImageSizeUnit` (`"50%"` or `"800"`/`"800px"`); `ImageManipulator._convert_unit_to_int` resolves percentages against the source image's dimensions, and `max_size` is resolved with no source (percentages are not meaningful there). A dimension of 0 means "derive from aspect ratio".
- `ImageManipulator` is lazy and chainable: the Pillow image opens on first `.image` access, and every mutator returns `self`.
- **Output format comes from the file extension.** `main.py` calls `image.save(out_file)` without a format, so `ImageFormat.Default` (`None`) lets Pillow infer it from the extension that `get_output_file` rewrote from `--format` (default `WEBP`). Changing the format therefore means changing the extension logic in `get_output_file`, not the `save` call.
- `get_output_file` has a side effect: it creates the output directory tree. It also appends the new extension rather than replacing it when the existing extension is 5+ characters.
- `CLI` is also the logger: `print` (respects `--quiet`), `verbose` (`--verbose`), `debug` (`DEV_MODE` env var), `exception`/`error` (stderr). `ImageManipulator` creates its own `CLI()` with default args (`/tmp /tmp`) when none is passed, so `verbose` output there only appears if a configured `CLI` is injected.
- `CLI.validate_args` has side effects: it creates the output folder and defaults it to `<input>_resized` when absent (though argparse still declares `output_folder` as a required positional).

## Work in flux: PLAN-00001

`docs/plans/00001-Python_314_Deps_CI_Security_Coverage.md` (approved) drives an in-progress Python 3.14 / dependency / CI / security / coverage update. The working tree may be mid-migration. `pyproject.toml` currently says `python = "^3.12"` while `.python-version` is `3.11.2` and the black/isort targets are `py311`, so the "pinned to 3.11" statement in `AGENTS.md` may be stale. Check the plan and the current files before relying on a Python version. Also note that the `[tool.coverage.run] command_line` still points at `unittest`, but tests and CI run through pytest.
