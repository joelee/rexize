---
title: "Delivery Plan 00001: Python 314 Deps CI Security Coverage"
aliases:
  - "Plan 00001"
tags:
  - delivery-plan
  - implementation
  - opencode
type: delivery-plan
plan_id: "PLAN-00001"
plan_status: draft
plan_kind: initial
created_at: "2026-09-29T17:04:16Z"
approved_at: null
planner_agent: DeliveryPlanner
planner_model: "zai-coding-plan/glm-5.3"
triggered_by: user
request_kind: direct
repository: "joelee/rexize"
baseline_branch: "master"
baseline_commit: "6c3b5ea5ee01cb97e4e12f9d7b2358d95909f5df"
source_ideas: []
source_reviews: []
previous_plan: null
requirements_count: 5
steps_count: 5
acceptance_criteria_count: 6
blocking_decisions: 0
build_ready: false
web_research_used: true
confidence: high

# Builder-maintained front matter. Builder may update only these keys after
# explicit user approval; Delivery Planner initializes them.
implementation_status: not-started
builder_agent: null
builder_model: null
execution_branch: null
execution_started_at: null
execution_updated_at: null
execution_completed_at: null
current_step: null
---

# Delivery Plan 00001: Python 314 Deps CI Security Coverage

> [!abstract] Plan status: `draft`
> Raise rexize's Python floor to 3.12 and support 3.14.x (supported range 3.12–3.14, dropping 3.11 per user direction), refresh all dependencies past every listed security-advisory floor, modernize the GitHub Actions CI with a 3.12–3.14 matrix, and raise enforced test coverage from 62% to 80%. All advisory floors and Python ranges were verified against current registry metadata; no blocking decisions remain.

## 1. Objective and outcome

The repository currently targets Python 3.11 only, carries dependency versions with published high/moderate CVEs (pillow 10.2.0, pytest 8.1.1, setuptools 69.2.0, virtualenv 20.25.1, filelock 3.13.3, pygments 2.17.2), runs CI on a single Python version with outdated action versions, and enforces only 62% test coverage. This plan delivers, in one safe sequence: a raised Python floor of 3.12 with support through 3.14.x (3.11 support dropped — an explicitly user-directed breaking change), a fully refreshed `poetry.lock` that clears every advisory floor the user listed, an updated `.github/workflows/python-app.yml` testing Python 3.12/3.13/3.14 with current action versions, and new tests lifting enforced coverage to ≥80%. User-visible CLI behaviour is unchanged.

## 2. Source traceability

| Requirement | Source | Source location | Interpretation |
|---|---|---|---|
| PLAN-00001-REQ-01 | User | Current request, item 1: "Support for Python 3.14.x"; amended by user instruction "Change floor to 3.12" | Supported Python range is 3.12–3.14: raise the floor to `python = "^3.12"` (dropping 3.11) and make the package, toolchain, and CI work through CPython 3.14.x (see DEC-01) |
| PLAN-00001-REQ-02 | User | Current request, item 2: "Update any outdated packages" | Refresh direct and transitive dependencies in `pyproject.toml`/`poetry.lock` to current releases that resolve across Python 3.12–3.14 |
| PLAN-00001-REQ-03 | User | Current request, item 4 plus the pasted dependency-advisory block (pillow <10.3.0 and <12.3.0; setuptools <70.0.0; virtualenv <20.26.6; filelock <3.20.1; Pygments <2.20.0; pytest <9.0.3, with listed CVEs incl. CVE-2024-28219, CVE-2024-6345, CVE-2024-53899, CVE-2026-54060/58/59, CVE-2026-55380, CVE-2026-59197/198/199/200, CVE-2026-55798, CVE-2025-71176, CVE-2025-68146, CVE-2025-47273, CVE-2026-22701/702, CVE-2026-4539, CVE-2026-59890) | Locked versions must meet or exceed every stated floor: pillow ≥12.3.0 (clears both pillow entries), setuptools ≥70.0.0, virtualenv ≥20.26.6, filelock ≥3.20.1, Pygments ≥2.20.0, pytest ≥9.0.3 |
| PLAN-00001-REQ-04 | User + Repository | Current request, item 3: "Implement the Github CI actions"; existing `.github/workflows/python-app.yml` | CI already exists; interpret as modernize and extend it (matrix across supported Pythons, current action versions, retained gates; triggers unchanged — see DEC-02) |
| PLAN-00001-REQ-05 | User | Current request, item 5: "Increase test coverage to 80% or above" | Total coverage ≥80.0% measured by the existing CI command and enforced by raising `[tool.coverage.report] fail_under` from 62 to 80 |

## 3. Repository baseline

| Field | Value |
|---|---|
| Repository | joelee/rexize (remote `git@github.com:joelee/rexize.git`) |
| Branch | master |
| HEAD | 6c3b5ea5ee01cb97e4e12f9d7b2358d95909f5df |
| Working tree at publication | Clean (the allocated plan file was the only in-flight artefact) |
| Applicable instructions | `/AGENTS.md` (repo root), `docs/plans/AGENTS.md` (plan-directory contract), `.opencode/agents/DeliveryPlanner.md` (normative for this planner) |

Verified baseline facts used by this plan: `pyproject.toml` (`python = "^3.11"`, `pillow = "^10.2.0"`, dev deps pytest `^8.0.1` / pytest-cov `^4.1.0` / pre-commit `^3.6.2` / flake8 `^7.0.0` / isort `^5.13.2` / icecream `^2.1.3`, classifier `Python :: 3.11` only, `fail_under = 62`, entry point `rexize = src.main:main`, `pythonpath = ["src"]`); `poetry.lock` (pillow 10.2.0, pytest 8.1.1, pytest-cov 4.1.0, pre-commit 3.7.0, flake8 7.0.0, isort 5.13.2, setuptools 69.2.0 via nodeenv←pre-commit, virtualenv 20.25.1, filelock 3.13.3, pygments 2.17.2 via icecream; lock python-versions `^3.11`); `.python-version` = `3.11.2`; `.pre-commit-config.yaml` (black 23.11.0 with `language_version: python3.11`, flake8 6.1.0, isort 5.12.0, plus `poetry check` local hook); `.github/workflows/python-app.yml` (triggers: all PRs + push to master/development; single Python 3.11 job; actions/checkout@v3, actions/setup-python@v4, actions/cache@v3, snok/install-poetry@v1, pre-commit/action@v3.0.1; test step `poetry run pytest --cov=src --cov-report=term-missing tests/`); `src/` modules import flat; no `.codegraph/` index.

## 4. Scope

### In scope

- `pyproject.toml` dependency constraints, classifiers, and coverage gate; regenerated `poetry.lock`.
- `.python-version` default toolchain bump; `README.md` supported-version note; root `AGENTS.md` Python-version references (3.11 pin → 3.12 floor).
- `.pre-commit-config.yaml` hook revision bumps needed to run on Python 3.14 (black, flake8, isort revs; black `language_version` line).
- `.github/workflows/python-app.yml`: 3.12–3.14 matrix, current action versions, retained pre-commit + coverage gates, unchanged triggers.
- New/extended tests under `tests/` to reach ≥80% total coverage, focused on currently untested code (`src/main.py` `main()`/`get_output_file()`, `CLI` output methods, `ImageManipulator` max-size and default-save paths, `FileIterator` custom filters).
- Minimal `src/` changes only if the 3.14 audit finds a real incompatibility (none is expected; see Risks).

### Out of scope

- Publishing a release to PyPI, changing `rexize` version `0.2.4`, or any release management (DEC-03).
- New features from the README TODO list (bulk renaming, rotation/cropping CLI options, GUI, user docs).
- Refactoring `src/` beyond what new tests require; changing CLI flags, defaults, exit codes, or output-tree behaviour.
- Converting `[tool.poetry]` to PEP 621 `[project]` metadata; switching build backend; adding dependencies.
- Reaching 90% coverage (README stretch goal) — this plan targets ≥80% exactly.
- Any work in `docs/ideas/`, `docs/reviews/`, or other numbered report directories.

## 5. Constraints and preserved decisions

- Package/module conventions preserved: package named `src`, flat imports (`from cli import CLI`), tests via `pythonpath = ["src"]`, entry point `rexize = src.main:main`, `bin/rexize` launcher.
- Style gates preserved: black line length 88, flake8 max-line-length 99 with E203 ignored, isort black profile, `poetry check` pre-commit hook.
- CI triggers preserved: all pull requests plus pushes to `master` and `development` (root `AGENTS.md` documents the branch model).
- Tests must keep running from the repo root (fixtures use relative `tests/data/...` paths).
- Exit codes preserved: 55 = invalid args, 1 = runtime error; `DEV_MODE` env var behaviour unchanged.
- Dependency security floors from the advisory are hard minimums, not targets: pillow ≥12.3.0, setuptools ≥70.0.0, virtualenv ≥20.26.6, filelock ≥3.20.1, Pygments ≥2.20.0, pytest ≥9.0.3.
- Coverage gate must be raised by actually covering code — `omit`/`exclude_lines` changes to game the percentage are forbidden.

## 6. Assumptions

None. Unresolved matters are recorded as decisions and block approval when material.

## 7. Decisions and blockers

| ID | Decision or blocker | Resolution | Owner | Status |
|---|---|---|---|---|
| DEC-01 | Python floor: the initial draft read "support for 3.14.x" additively (keep `^3.11`); the user then directed "Change floor to 3.12". Final decision: `python = "^3.12"`, supported and tested range 3.12–3.14, 3.11 support dropped (accepted breaking change). Verified feasible: pillow 12.3.0 and pytest 9.0.3 both require Python ≥3.10. | Explicit user instruction during draft review (2026-09-29); the superseded additive reading is preserved in the Planning change log | User | Resolved |
| DEC-02 | "Implement the GitHub CI actions" read as modernize/extend the existing `python-app.yml` (CI already exists): version matrix, current action versions, retained gates, triggers unchanged. | Repo evidence: workflow already runs pre-commit + coverage pytest on every PR/push to master/development | User (veto at draft review) | Resolved |
| DEC-03 | No `rexize` version bump and no PyPI publish in this plan; release cadence stays a user decision. | Not requested; avoids release side effects | User | Resolved |

## 8. Affected architecture and components

Confirmed paths and symbols:

- `pyproject.toml` — `[tool.poetry.dependencies]` (python `^3.11` → `^3.12`, pillow), `[tool.poetry.group.dev.dependencies]` (pytest, pytest-cov, pre-commit, flake8, isort, icecream), `classifiers` (replace `Python :: 3.11` with 3.12/3.13/3.14), `[tool.coverage.report] fail_under`.
- `poetry.lock` — full regeneration; transitive security floors arrive via pre-commit (→ virtualenv → filelock; → nodeenv → setuptools) and icecream (→ pygments).
- `.python-version` — dev toolchain default, `3.11.2` → `3.14`.
- `.pre-commit-config.yaml` — hook revs for black/flake8/isort; remove black's `language_version: python3.11` pin so hooks follow the active interpreter.
- `.github/workflows/python-app.yml` — matrix + action versions + gates (REQ-04 invariants in STEP-04).
- `tests/test_main.py` (new) — `src/main.py::get_output_file`, `main()` exit paths (0/55/1).
- `tests/test_cli_argparser.py` or new `tests/test_cli_output.py` — `CLI.print/error/verbose/debug/exception/exit`, quiet flag, `DEV_MODE`, default-args property.
- `tests/test_image_manipulator.py` — `resize` with `max_size` (both dimension branches), `save()` default destination.
- `tests/test_file_iterator.py` — `add_filter` custom predicate chaining, `directory` property.
- `README.md` — one line noting tested Python versions.
- `/AGENTS.md` (root) — Python-pin references updated to the 3.12 floor / 3.14 default.
- `src/**` — read-only audit for 3.14 incompatibilities; change only on a found defect.

No interface, schema, or data-store changes. The dependency chain carrying the transitive advisals is the only structural relationship that matters: pre-commit → virtualenv → filelock, pre-commit → nodeenv → setuptools, icecream → pygments.

## 9. Requirement catalogue

### PLAN-00001-REQ-01 — Python 3.12 floor with 3.14.x support

- **Requirement:** The Python requirement becomes `python = "^3.12"` (3.11 dropped per user direction); the package installs, the test suite passes, and the CLI runs correctly on CPython 3.12–3.14; classifiers list 3.12/3.13/3.14 (3.11 removed).
- **Rationale:** User item 1. Current code uses only stable APIs (`typing.Self`, `argparse`, `os.walk`, Pillow core calls), so support is a toolchain/metadata exercise unless the audit finds otherwise.
- **Source:** User request item 1 as amended ("Change floor to 3.12"); `pyproject.toml`; verified PyPI metadata for pillow 12.3.0 and pytest 9.0.3 (both require Python ≥3.10 only).
- **Acceptance evidence:** `poetry run pytest` green under 3.12 and 3.14 environments; classifiers updated (no 3.11 entry); `bin/rexize` smoke run on 3.14 exits 0; CI matrix legs 3.12/3.13/3.14 green.

### PLAN-00001-REQ-02 — Update outdated packages

- **Requirement:** Direct dependencies (pillow, pytest, pytest-cov, pre-commit, flake8, isort; icecream refreshed within its constraint) are raised to current releases that resolve across Python 3.12–3.14, and `poetry.lock` is regenerated with hashes.
- **Rationale:** User item 2; also a prerequisite for REQ-01 (old pinned majors predate 3.14 wheels/tooling).
- **Source:** User request item 2; `pyproject.toml` `[tool.poetry.dependencies]`/`[tool.poetry.group.dev.dependencies]`; `poetry.lock` current versions.
- **Acceptance evidence:** `poetry lock` resolves without solver errors; `poetry check` passes; full test suite green on updated deps; `poetry.lock` versions are at least the REQ-03 floors.

### PLAN-00001-REQ-03 — Clear all listed security advisories

- **Requirement:** Locked versions meet: pillow ≥12.3.0, setuptools ≥70.0.0, virtualenv ≥20.26.6, filelock ≥3.20.1, Pygments ≥2.20.0, pytest ≥9.0.3 — clearing both pillow advisory entries (<10.3.0 and <12.3.0) and every listed CVE.
- **Rationale:** User item 4 with the pasted advisory block; direct floors via constraint bumps, transitive floors via the refreshed lock (pre-commit/icecream chains).
- **Source:** User request item 4 and advisory block; `poetry.lock` lines for the six packages.
- **Acceptance evidence:** Inspection of `poetry.lock` shows each floor met (work-log table quoting name/version pairs); no constraint in `pyproject.toml` caps any of them below its floor.

### PLAN-00001-REQ-04 — Modernized GitHub Actions CI

- **Requirement:** `python-app.yml` runs pre-commit (`--all-files`) at least once and the coverage-gated pytest (`poetry run pytest --cov=src --cov-report=term-missing tests/`) on a matrix of Python 3.12, 3.13, 3.14, using current action versions (checkout v7, setup-python v7; snok/install-poetry@v1 and pre-commit/action@v3.0.1 remain latest), with poetry dependency caching retained and triggers unchanged.
- **Rationale:** User item 3; single-version CI cannot prove REQ-01, and v3/v4-era actions are outdated (latest releases verified: checkout v7.0.1 and setup-python v7.0.0, both 2026-07-20; pre-commit/action v3.0.1 still latest).
- **Source:** User request item 3; `.github/workflows/python-app.yml`; GitHub releases API (accessed 2026-09-29).
- **Acceptance evidence:** Workflow file matches the invariants above and passes `check-yaml` in pre-commit; a PR run executes all three matrix legs green (run URL recorded in work log).

### PLAN-00001-REQ-05 — Test coverage ≥80%, enforced

- **Requirement:** Total coverage of `src` reaches ≥80.0% under the CI measurement command, and the gate is enforced by `[tool.coverage.report] fail_under = 80`.
- **Rationale:** User item 5; current gate is 62 and `src/main.py` (roughly a sixth of `src` statements) is entirely untested, plus `CLI` output methods and `ImageManipulator` max-size paths.
- **Source:** User request item 5; `pyproject.toml` line 54 (`fail_under = 62`); test files read at baseline show no tests importing `main` and none exercising `max_size`/`print`/`quiet`/`verbose`/`debug`/`exit`.
- **Acceptance evidence:** `poetry run pytest --cov=src --cov-report=term-missing tests/` reports TOTAL ≥80% and exits 0 with the raised gate; per-file report shows `src/main.py` no longer near 0%.

## 10. Delivery strategy

Dependency-first sequencing, each step independently verifiable and leaving the repo green:

1. **STEP-01 (floor + deps + security)** must come first: it raises the Python constraint to `^3.12` so the lock regenerates exactly once under the new range, and nothing on 3.14 installs with pillow ^10.2 anyway; the advisory floors are pure lock/constraint work verifiable without touching code.
2. **STEP-02 (3.14 enablement on the 3.12 floor)** uses those deps; its audit also bumps pre-commit hook revs so lint tooling runs on 3.14.
3. **STEP-03 (coverage)** is pure test addition plus the gate raise (gate raised only after the measured total is ≥80, so no intermediate red state).
4. **STEP-04 (CI)** lands last so the first run of the new matrix + 80% gate is already satisfied; CI only runs on PRs and pushes to master/development, so verification is via a PR.
5. **STEP-05 (full gate)** repeats every quality command on both 3.12 and 3.14, runs the CLI smoke test, and finalizes evidence.

TDD note: STEP-03's deliverable *is* tests, so the fail-first loop applies to STEP-02's audit and STEP-04's config only in the sense of running existing suites after each change; the coverage tests themselves pass immediately against current behaviour and that is the point (locking in behaviour before/alongside dependency majors). Rollback at every step is `git revert` of that step's commits; there are no migrations or external state.

## 11. Detailed implementation steps

### PLAN-00001-STEP-01 — Raise Python floor to 3.12, refresh dependencies, clear advisory floors

- **Status placeholder:** `not-started`
- **Objective:** Python constraint set to `^3.12`, all direct constraints raised, lock regenerated under the new range, every advisory floor verifiably met, suite green on a 3.12 environment.
- **Requirements:** `PLAN-00001-REQ-01` (floor constraint), `PLAN-00001-REQ-02`, `PLAN-00001-REQ-03`
- **Depends on:** None
- **Affected components:** `pyproject.toml`, `poetry.lock`
- **Preconditions:** Clean worktree on the execution branch; `poetry install` works at baseline; a Python 3.12 interpreter is available locally (`poetry env use 3.12`).
- **Test or evidence first:** Record the baseline suite result (`poetry run pytest`) before any change, so any post-bump failure is attributable.
- **Implementation tasks:**
  1. In `pyproject.toml`, set `python = "^3.12"` (user-directed floor; 3.11 dropped), set `pillow = "^12.3"` (mandatory floor; clears both pillow advisories), and raise dev constraints: `pytest = "^9.0.3"` (mandatory floor), and pytest-cov / pre-commit / flake8 / isort to the latest releases that resolve for Python 3.12–3.14 (`icecream` stays `^2.1.3`; refreshed transitively). Exact pins above the floors are Builder's bounded decision via poetry resolution; floors are not negotiable.
  2. Switch the poetry env to 3.12 (`poetry env use 3.12`), then run `poetry update` to regenerate `poetry.lock` (now locked for `^3.12`) and the environment within the new constraints.
  3. Inspect `poetry.lock` and confirm floors: pillow ≥12.3.0, setuptools ≥70.0.0, virtualenv ≥20.26.6, filelock ≥3.20.1, pygments ≥2.20.0, pytest ≥9.0.3. If a transitive floor is not met (e.g., an old `nodeenv`/`virtualenv` pin), run targeted `poetry update <package>` until met; never hand-edit `poetry.lock`.
  4. Fix any test failures caused by pytest 8→9 or Pillow 10→12 behaviour changes (suite is small; expected churn is minimal — see Risks).
- **Documentation/configuration/operations:** None beyond the files listed.
- **Verification:** `poetry check` exits 0; `poetry run pytest` green under the 3.12 env; lock metadata shows `python-versions = "^3.12"`; lock inspection table (six name/version pairs) recorded in the work log.
- **Completion criteria:** All six floors met in `poetry.lock`; lock locked to `^3.12`; suite green; `poetry check` passes.
- **Rollback or recovery:** `git checkout -- pyproject.toml poetry.lock && poetry install` restores baseline deps.
- **Builder stop conditions:** Poetry cannot satisfy constraints simultaneously on `^3.12` (solver conflict) — stop and report the conflict rather than raising the Python floor beyond 3.12; a pillow/pytest major breaking the suite in ways requiring changes to `src/` behaviour — stop and report before altering behaviour.

### PLAN-00001-STEP-02 — Enable Python 3.14.x on the 3.12 floor

- **Status placeholder:** `not-started`
- **Objective:** Toolchain, metadata, and lint hooks work on 3.14; 3.12 floor intact.
- **Requirements:** `PLAN-00001-REQ-01`
- **Depends on:** `PLAN-00001-STEP-01`
- **Affected components:** `pyproject.toml` (classifiers), `.python-version`, `.pre-commit-config.yaml`, `README.md`, `src/**` (audit only)
- **Preconditions:** STEP-01 complete (deps resolvable on 3.14).
- **Test or evidence first:** Baseline: `poetry run python --version` and suite result under the current 3.12 env.
- **Implementation tasks:**
  1. Replace the `Programming Language :: Python :: 3.11` classifier with `:: 3.12`, `:: 3.13`, `:: 3.14` (the `python = "^3.12"` constraint is already set in STEP-01).
  2. Set `.python-version` to `3.14` (minor-version form so tooling picks the latest 3.14.x).
  3. Audit `src/` for 3.12–3.14 removals/deprecations (`distutils`, removed `argparse`/`os`/`enum` behaviours, `typing.Self` is 3.11+ and fine). Expected result: no changes; if a real incompatibility exists, fix it minimally and add a regression test.
  4. Bump `.pre-commit-config.yaml` hook revs: black 23.11.0 → current, flake8 6.1.0 → current (7.x line), isort 5.12.0 → current (6.x line); delete black's `language_version: python3.11` so hooks use the active interpreter. Keep all other hooks as-is.
  5. Run `pre-commit run --all-files`; accept/commit any reformatting black produces (config line length 88 is unchanged).
  6. Verify on 3.14: `poetry env use 3.14 && poetry install && poetry run pytest`; then re-verify the floor: `poetry env use 3.12 && poetry run pytest`.
  7. Update `README.md` Prerequisites to state Python 3.12+ with CI-tested versions 3.12–3.14; update the root `AGENTS.md` Python-pin references ("pinned to 3.11", `python = "^3.11"`) to the 3.12 floor.
- **Documentation/configuration/operations:** README note; classifier metadata for the next publish.
- **Verification:** Both env runs green; `pre-commit run --all-files` exits 0; `poetry run python --version` shows 3.14.x in the 3.14 env.
- **Completion criteria:** Suite green on 3.14 and 3.12; hooks pass; metadata updated.
- **Rollback or recovery:** Revert the step's commits; `poetry env use 3.12`.
- **Builder stop conditions:** A hook rev with no 3.14-compatible release (pin the newest compatible rev and note it); a `src/` incompatibility whose fix would change CLI behaviour — stop and report.

### PLAN-00001-STEP-03 — Raise enforced coverage to ≥80%

- **Status placeholder:** `not-started`
- **Objective:** Cover the untested paths and enforce 80%.
- **Requirements:** `PLAN-00001-REQ-05`
- **Depends on:** `PLAN-00001-STEP-01` (suite must already be green on updated deps; independent of STEP-02 in content, but execute after it to keep one verification context)
- **Affected components:** `tests/test_main.py` (new), `tests/test_cli_argparser.py` (extend) or `tests/test_cli_output.py` (new), `tests/test_image_manipulator.py` (extend), `tests/test_file_iterator.py` (extend), `pyproject.toml` (`fail_under`)
- **Preconditions:** Suite green; tests run from repo root.
- **Test or evidence first:** Run `poetry run pytest --cov=src --cov-report=term-missing tests/` and record the baseline TOTAL and per-file gaps in the work log before writing tests.
- **Implementation tasks:**
  1. `tests/test_main.py`: unit-test `get_output_file` (tree mirroring, extension rewrite, `jpeg`→`jpg` mapping, trailing-slash output folder, long-extension append branch, output-dir creation) using a lightweight args namespace; test `main()` happy path (monkeypatched `sys.argv`, temp input containing a copy of `tests/data/test_img.png`, assert `SystemExit` code 0 and output file exists), invalid-args path (missing width/height/max-size → `SystemExit` 55), and runtime-error path (corrupt `.png` fixture → `SystemExit` 1).
  2. CLI output methods: `print` vs `-q/--quiet` suppression, `error` to stderr, `verbose` under `--verbose`, `debug` under `DEV_MODE` (monkeypatch env), `exception`, `exit(status)` raising `SystemExit`, default-args property (`CLI()` with no argv uses `DEFAULT_CLI_ARGS`).
  3. `ImageManipulator`: `resize` with `max_size` covering both dimension branches (wide and tall images; assert resulting dims ≤ max_size and aspect ratio preserved), `save()` with no `dest_path` producing the `-rexised` sibling file.
  4. `FileIterator`: `add_filter` with a custom predicate, chained with `filter_by_extension`; `directory` property.
  5. Re-run coverage; if TOTAL < 80%, use the per-file missing report to add the next-highest-value tests (no `omit`/`exclude_lines` changes allowed).
  6. Only once TOTAL ≥ 80: set `[tool.coverage.report] fail_under = 80` and re-run the CI command to prove the gate holds.
- **Documentation/configuration/operations:** None.
- **Verification:** `poetry run pytest --cov=src --cov-report=term-missing tests/` → TOTAL ≥80.0%, exit 0, with `fail_under = 80` active; record TOTAL and key per-file numbers in the work log.
- **Completion criteria:** Gate raised and passing; `src/main.py` materially covered (no longer ~0%).
- **Rollback or recovery:** Revert tests + gate commit; gate and tests land together so no red intermediate.
- **Builder stop conditions:** Coverage plateaus below 80 after the enumerated areas are covered — stop, report the measured TOTAL and remaining gaps, and request a decision (do not weaken measurement); tests requiring behaviour changes to pass — stop and report.

### PLAN-00001-STEP-04 — Modernize the GitHub Actions workflow

- **Status placeholder:** `not-started`
- **Objective:** Matrix CI on 3.12–3.14 with current actions and retained gates.
- **Requirements:** `PLAN-00001-REQ-04` (also operationalizes REQ-01/03/05 evidence)
- **Depends on:** `PLAN-00001-STEP-02`, `PLAN-00001-STEP-03`
- **Affected components:** `.github/workflows/python-app.yml`
- **Preconditions:** Steps 01–03 complete and green locally on both 3.12 and 3.14.
- **Test or evidence first:** `pre-commit run check-yaml --files .github/workflows/python-app.yml` (hook already configured) after editing.
- **Implementation tasks:**
  1. Recommended shape (invariants matter more than exact layout): a `lint` job on Python 3.14 running `pre-commit/action@v3.0.1` with `extra_args: --all-files` after poetry install; a `test` job with `strategy.matrix.python-version: ["3.12", "3.13", "3.14"]` (no `fail-fast: false` needed, but acceptable).
  2. Use `actions/checkout@v7` and `actions/setup-python@v7` (with `python-version: ${{ matrix.python-version }}` and `cache: poetry`); keep `snok/install-poetry@v1`; drop the manual `actions/cache@v3` venv step if `cache: poetry` covers it, otherwise retain an equivalent cache.
  3. Test step stays exactly: `poetry run pytest --cov=src --cov-report=term-missing tests/` (now enforcing 80 via config).
  4. Keep `on:` triggers (all PRs; pushes to master/development) and `permissions: contents: read`.
- **Documentation/configuration/operations:** None (workflow is self-documenting).
- **Verification:** `pre-commit run --all-files` passes including `check-yaml`; open a PR (or push to `development`) so CI triggers; confirm all matrix legs and the lint job are green; record the run URL.
- **Completion criteria:** PR run green across 3.12/3.13/3.14 + lint; invariants satisfied.
- **Rollback or recovery:** `git revert` of the workflow commit restores the previous pipeline.
- **Builder stop conditions:** A matrix leg fails from an environment/dependency issue Builder cannot fix without scope changes — stop and report the failing leg's log excerpt; GitHub-hosted 3.14 unavailable (not expected) — stop and report rather than dropping the leg.

### PLAN-00001-STEP-05 — Full verification gate and completion evidence

- **Status placeholder:** `not-started`
- **Objective:** One coherent, recorded proof that every requirement is met.
- **Requirements:** `PLAN-00001-REQ-01`, `PLAN-00001-REQ-02`, `PLAN-00001-REQ-03`, `PLAN-00001-REQ-04`, `PLAN-00001-REQ-05`
- **Depends on:** `PLAN-00001-STEP-04`
- **Affected components:** none (verification only; work log updates)
- **Preconditions:** All prior steps complete.
- **Test or evidence first:** Not applicable (this step is the evidence).
- **Implementation tasks:**
  1. On 3.14 env: `poetry check`; `pre-commit run --all-files`; `poetry run pytest --cov=src --cov-report=term-missing tests/` (TOTAL ≥80).
  2. On 3.12 env: `poetry run pytest` (green).
  3. Smoke: `bin/rexize <tmp_input> <tmp_output> -W 50% -f WEBP` on 3.14 — exits 0, output tree created, exit codes 55/1 spot-checked with bad args (missing size) and a bad input folder.
  4. Confirm lock floors one final time; confirm README/`pyproject.toml` consistency (versions, classifiers).
  5. Fill the Verification results and Completion summary tables; set Builder front matter to completed.
- **Documentation/configuration/operations:** Work-log completion only.
- **Verification:** Every command above exits 0 / expected codes; evidence rows in the work log.
- **Completion criteria:** All acceptance criteria (section 14) checkable from work-log evidence.
- **Rollback or recovery:** Not applicable (verification step).
- **Builder stop conditions:** Any gate failing here after earlier steps passed — re-open the responsible step's notes and report before any rework.

## 12. Cross-cutting concerns

| Area | Applicability | Planned action or reason not applicable | Step or requirement |
|---|---|---|---|
| Compatibility and APIs | Applicable | Preserve CLI flags/exit codes; raise Python floor to `^3.12`, dropping 3.11 (user-directed breaking change, DEC-01); Pillow/pytest majors audited against actual usage | STEP-01, STEP-02, REQ-01 |
| Data and migration | Not applicable | No persistent data or schemas; only lockfile regeneration | — |
| Security and privacy | Applicable | Enforce the six advisory floors (17+ CVEs listed); lock hashes retained; no new secrets or external calls | STEP-01, REQ-03 |
| Performance and scale | Not applicable | No hot-path changes; Pillow 12 performance differences are incidental | — |
| Reliability and failure handling | Not applicable | Failure paths (exit 55/1) unchanged and newly locked in by tests | STEP-03 |
| Observability and operations | Not applicable | CLI output (`--quiet`/`--verbose`/`DEV_MODE`) unchanged, now covered by tests | STEP-03 |
| Dependencies and supply chain | Applicable | Major-bump risk managed by full suite + smoke run; pillow 12.3.0 published via PyPI trusted publishing (verified) | STEP-01, REQ-02 |
| Accessibility and UX | Not applicable | CLI interface untouched | — |
| Documentation and release | Applicable | README supported-versions line updated; PyPI publish/version bump explicitly deferred (DEC-03) | STEP-02, STEP-05 |
| Deployment and rollback | Applicable | CI workflow is the only deployment surface; per-step `git revert` restores prior pipeline; CI verified via PR before merge | STEP-04 |

## 13. Verification strategy

| Level | Evidence or command | When | Required result |
|---|---|---|---|
| Dependency integrity | `poetry check` | STEP-01, STEP-05 | Exit 0 |
| Advisory floors | `poetry.lock` inspection: pillow ≥12.3.0, setuptools ≥70.0.0, virtualenv ≥20.26.6, filelock ≥3.20.1, pygments ≥2.20.0, pytest ≥9.0.3 | STEP-01, STEP-05 | All six floors met |
| Unit/component tests | `poetry run pytest` (3.12 env and 3.14 env) | Every step; both envs in STEP-02/05 | All green |
| Coverage gate | `poetry run pytest --cov=src --cov-report=term-missing tests/` | STEP-03, STEP-05 | TOTAL ≥80.0%, exit 0 with `fail_under = 80` |
| Static analysis / lint | `pre-commit run --all-files` (black, flake8, isort, check-yaml incl. workflow, poetry check hook) | STEP-02, STEP-04, STEP-05 | Exit 0 |
| End-to-end smoke | `bin/rexize <in> <out> -W 50% -f WEBP`; bad-args → 55; bad folder → 1 | STEP-05 | Exit 0 / 55 / 1 respectively; output files present |
| CI pipeline | PR (or push to `development`) Actions run | STEP-04 | lint job + 3.12/3.13/3.14 legs green |
| Rollback | `git revert` of step commits (dry-run not required) | If needed | Repo returns to prior green state |

## 14. Acceptance criteria

- [ ] `PLAN-00001-AC-01` `poetry.lock` contains pillow ≥12.3.0, setuptools ≥70.0.0, virtualenv ≥20.26.6, filelock ≥3.20.1, Pygments ≥2.20.0, pytest ≥9.0.3 (clearing both pillow advisories and all listed CVEs).
- [ ] `PLAN-00001-AC-02` `pyproject.toml` sets `python = "^3.12"`, lists classifiers 3.12/3.13/3.14 with the 3.11 entry removed, and sets `fail_under = 80`; `poetry.lock` metadata shows `^3.12`; `.python-version` is a 3.14 value; README and root `AGENTS.md` state the 3.12+ / tested 3.12–3.14 range.
- [ ] `PLAN-00001-AC-03` `poetry run pytest --cov=src --cov-report=term-missing tests/` passes with TOTAL coverage ≥80.0% under the raised gate, in both 3.12 and 3.14 local environments.
- [ ] `PLAN-00001-AC-04` `bin/rexize` smoke run on 3.14 processes an image (exit 0, output written); invalid args exit 55; runtime failure exits 1.
- [ ] `PLAN-00001-AC-05` `.github/workflows/python-app.yml` tests the 3.12–3.14 matrix with checkout v7 / setup-python v7, runs `pre-commit --all-files` at least once, retains the exact coverage pytest command and unchanged triggers, and a PR Actions run is green on all legs.
- [ ] `PLAN-00001-AC-06` `poetry check` and `pre-commit run --all-files` exit 0 at final state, with evidence recorded in the Builder Work Log.

## 15. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation or test | Owner/step |
|---|---|---|---|---|
| Pillow 10→12 breaks image operations | Low | High | Code audit shows only stable APIs (`open/resize/convert/rotate/save`); full suite + STEP-05 smoke run | Builder/STEP-01,05 |
| pytest 8→9 breaks test collection/asserts | Low | Medium | Small suite; run immediately after bump; fix deprecations | Builder/STEP-01 |
| Newer black reformats existing files | High | Low | Line-length 88 config preserved; reformatting committed as an isolated commit | Builder/STEP-02 |
| Coverage stalls just under 80 | Medium | Medium | `src/main.py` + CLI methods + max-size paths are the known gap (~enough headroom); stop-and-report rule forbids gaming the gate | Builder/STEP-03 |
| pre-commit 4.x / hook revs incompatible with 3.14 | Low | Medium | Rev bumps verified by `pre-commit run --all-files` on 3.14; pin newest compatible rev and note if blocked | Builder/STEP-02 |
| Poetry solver conflict across `^3.12` range | Low | High | Verified pillow 12.3.0 / pytest 9.0.3 require only ≥3.10; stop condition triggers user decision, not a silent floor raise beyond 3.12 | Builder/STEP-01 |
| CI matrix leg flaky/failing on GitHub runners | Low | Medium | Verify via PR before merge; leg logs recorded in work log | Builder/STEP-04 |

## 16. Builder hand-off

- **Start condition:** User approval and a clean repository.
- **First step:** `PLAN-00001-STEP-01` — dependency refresh and advisory floors.
- **Required sequence:** STEP-01 → STEP-02 → STEP-03 → STEP-04 → STEP-05 (coverage and 3.14 steps both depend on the dependency step; CI lands after coverage so the first matrix run is green).
- **Parallel-safe work:** None recommended; the sequence is short and strictly ordered. Test writing (STEP-03) may be drafted alongside STEP-02 but committed after it.
- **Do not change:** approved scope, requirements, steps, acceptance criteria, or content outside Builder's permitted work-log area; CLI behaviour; CI triggers; the coverage measurement command; advisory floors (downward).
- **Escalate when:** a poetry solver conflict forces raising the Python floor beyond 3.12; coverage cannot reach 80 without weakening measurement or changing behaviour; a matrix leg fails for upstream reasons; any `src/` change beyond a minimal 3.14 compatibility fix appears necessary.
- **Completion hand-off:** Work log with all verification rows filled (lock-floor table, coverage totals per env, CI run URL, smoke evidence), Builder front matter set to completed, and a note that REQ-03 can be re-verified by re-reading `poetry.lock`; suggest a Code Review for the dependency/CI commits.

<!-- BUILDER_WORK_LOG_START -->
## 17. Builder Work Log

> [!warning] Builder-maintained section
> Delivery Planner creates this section. After approval, Builder may update only
> this delimited section and the Builder-maintained front-matter fields. Builder
> must preserve prior entries and use UTC timestamps.

### Step status

| Step | Status | Started (UTC) | Completed (UTC) | Evidence | Builder notes |
|---|---|---|---|---|---|
| PLAN-00001-STEP-01 | not-started | — | — | — | — |
| PLAN-00001-STEP-02 | not-started | — | — | — | — |
| PLAN-00001-STEP-03 | not-started | — | — | — | — |
| PLAN-00001-STEP-04 | not-started | — | — | — | — |
| PLAN-00001-STEP-05 | not-started | — | — | — | — |

Allowed status values: `not-started`, `in-progress`, `blocked`, `completed`,
`skipped`. A skipped step requires explicit user approval recorded in Evidence.

### Execution log

| Timestamp (UTC) | Step | Event | Evidence or reference | Next action |
|---|---|---|---|---|

### Deviations and blockers

| Timestamp (UTC) | Step | Deviation or blocker | Impact | Decision required from |
|---|---|---|---|---|

None

### Verification results

| Timestamp (UTC) | Step | Command or check | Result | Evidence |
|---|---|---|---|---|

### Completion summary

- **Implementation status:** `not-started`
- **Completed requirements:** None
- **Incomplete requirements:** All
- **Outstanding blockers:** None
- **Review request:** Not ready
<!-- BUILDER_WORK_LOG_END -->

## 18. Planning change log

| Timestamp (UTC) | Plan status | Change | Reason | Requested/approved by |
|---|---|---|---|---|
| 2026-09-29T17:04:16Z | draft | Initial draft published (5 requirements, 5 steps, 6 acceptance criteria) | User request: Python 3.14.x support, package updates, CI implementation, listed security advisories, ≥80% coverage | DeliveryPlanner |
| 2026-09-29T22:46:41Z | draft | Python floor changed from `^3.11` to `^3.12` per user correction; supported/tested range now 3.12–3.14 (3.11 dropped, DEC-01 re-resolved as user-directed); STEP-01 takes the python-constraint change so the lock regenerates once; CI matrix, classifiers, verification envs (3.12 + 3.14), root `AGENTS.md` alignment, and AC-02/03/05 updated | User instruction "Change floor to 3.12" | User |

## 19. External references

- PyPI, "pillow 12.3.0" release metadata (requires_python `>=3.10`; classifiers 3.10–3.15; cp311/cp314 wheels present; released 2026-07-01, trusted publishing). Python Package Index. Accessed 2026-09-29. https://pypi.org/project/pillow/12.3.0/
- PyPI, "pytest 9.0.3" release metadata via JSON API (requires_python `>=3.10`; classifiers 3.10–3.14; released 2026-04-07). Python Package Index. Accessed 2026-09-29. https://pypi.org/pypi/pytest/9.0.3/json
- GitHub Releases API, "actions/checkout" latest release v7.0.1 (published 2026-07-20). Accessed 2026-09-29. https://api.github.com/repos/actions/checkout/releases/latest
- GitHub Releases API, "actions/setup-python" latest release v7.0.0 (published 2026-07-20). Accessed 2026-09-29. https://api.github.com/repos/actions/setup-python/releases/latest
- GitHub Releases API, "pre-commit/action" latest release v3.0.1 (published 2024-02-07; still latest). Accessed 2026-09-29. https://api.github.com/repos/pre-commit/action/releases/latest

## 20. Confidence

**High.** Every advisory floor, Python-range decision, and action version was verified against current registry/release metadata rather than assumed, and all repository facts (constraints, lock versions, workflow shape, coverage config, untested code paths) were read directly at baseline `6c3b5ea`. Residual uncertainty is limited to exact dev-tool pin choices (left to poetry resolution with mandatory floors) and the true current coverage percentage, which STEP-03 measures before writing tests.
