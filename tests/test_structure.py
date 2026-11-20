"""Checks repository invariants: syntax of all Python files, test coverage, and module layout."""

from __future__ import annotations

import py_compile
from pathlib import Path

import pytest

from tests.conftest import REPO_ROOT
from tests.test_mcp_servers import COVERED_SERVERS
from tests.test_python_scripts import COVERED_SCRIPTS

# output/ folders are generated and gitignored; a coding agent demo copies a whole project into one.
IGNORED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", "output"}


def _all_repo_python_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.py")):
        if any(part in IGNORED_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        files.append(path)
    return files


def _all_modules() -> list[Path]:
    return sorted(
        path for path in REPO_ROOT.glob("day-*/module-*") if path.is_dir()
    )


@pytest.mark.offline
@pytest.mark.parametrize(
    "py_file",
    _all_repo_python_files(),
    ids=[str(p.relative_to(REPO_ROOT)) for p in _all_repo_python_files()],
)
def test_python_file_compiles(py_file: Path, tmp_path: Path) -> None:
    """Catch syntax errors in every .py file, even ones skipped due to missing API keys."""
    compiled = tmp_path / f"{py_file.stem}.pyc"
    py_compile.compile(str(py_file), cfile=str(compiled), doraise=True)


@pytest.mark.offline
def test_every_python_file_is_registered_in_tests() -> None:
    """Fail if a new demo, playground, or server is added without adding it to tests/."""
    course_files = {
        str(path.relative_to(REPO_ROOT))
        for path in _all_repo_python_files()
        if path.relative_to(REPO_ROOT).parts[0] != "tests"
    }
    covered = COVERED_SCRIPTS | COVERED_SERVERS
    uncovered = sorted(course_files - covered)
    missing_files = sorted(path for path in covered if not (REPO_ROOT / path).is_file())

    assert not missing_files, f"Tests reference Python files that no longer exist: {missing_files}"
    assert not uncovered, (
        "Every Python script/server in the repo must be registered in "
        f"tests/test_python_scripts.py or tests/test_mcp_servers.py. Uncovered: {uncovered}"
    )


@pytest.mark.offline
@pytest.mark.parametrize(
    "module_dir",
    _all_modules(),
    ids=[str(m.relative_to(REPO_ROOT)) for m in _all_modules()],
)
def test_module_follows_guide_layout(module_dir: Path) -> None:
    """Check the standard folder layout described in MODULE_GUIDE.md."""
    assert (module_dir / "README.md").is_file()
    assert (module_dir / "slides" / "src" / "slides.js").is_file()
    assert (module_dir / "demo").is_dir()
    assert list((module_dir / "demo").glob("*.py")), f"{module_dir.name} has no demo scripts"
    assert (module_dir / "playground" / "README.md").is_file()
    assert (module_dir / "further-reading" / "README.md").is_file()

    day_readme = (module_dir.parent / "README.md").read_text(encoding="utf-8")
    assert module_dir.name in day_readme, (
        f"{module_dir.name} is missing from {module_dir.parent.name}/README.md"
    )
