"""Course-wide test suite for Agent Engineering.

Run everything available on this machine (skips missing API keys / local models):
    uv run pytest

Fast offline run (no network, API keys, Ollama, or Hugging Face downloads):
    uv run pytest --offline

Run just one area:
    uv run pytest -m slides
    uv run pytest -k module-01
"""

from __future__ import annotations

import functools
import importlib.util
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
API_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "XAI_API_KEY",
    "OPENROUTER_API_KEY",
)
PLACEHOLDER_VALUES = {"", "your-key-here"}

load_dotenv(REPO_ROOT / ".env")


def find_module(slug: str) -> str:
    """Resolve a module folder by slug (e.g. 'tools' -> 'day-one/module-03-tools')."""
    matches = sorted(REPO_ROOT.glob(f"day-*/module-*-{slug}"))
    assert len(matches) == 1, f"Expected one module matching *-{slug}, found {matches}"
    return str(matches[0].relative_to(REPO_ROOT))


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--offline",
        action="store_true",
        default=False,
        help="Skip tests that use the network, hosted APIs, Ollama, or Hugging Face models.",
    )


def has_api_key(name: str) -> bool:
    value = os.environ.get(name, "").strip()
    return value not in PLACEHOLDER_VALUES


def clean_env(*, strip_keys: bool = False) -> dict[str, str]:
    """Return a copy of os.environ with placeholder API keys removed."""
    env = dict(os.environ)
    # Prevent scripts' own load_dotenv() calls from reloading placeholder keys if stripped.
    for key in API_KEYS:
        if strip_keys or not has_api_key(key):
            env.pop(key, None)
    return env


@functools.cache
def ollama_models() -> frozenset[str]:
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as response:
            payload = json.load(response)
    except Exception:
        return frozenset()

    names: set[str] = set()
    for model in payload.get("models", []):
        name = model.get("name", "")
        if name:
            names.add(name)
            if name.endswith(":latest"):
                names.add(name.removesuffix(":latest"))
    return frozenset(names)


@functools.cache
def has_local_extra() -> bool:
    return (
        importlib.util.find_spec("torch") is not None
        and importlib.util.find_spec("transformers") is not None
    )


@functools.cache
def has_internet() -> bool:
    try:
        request = urllib.request.Request(
            "https://openrouter.ai/api/v1/models",
            headers={"User-Agent": "AgentEngineeringTests/1.0"},
        )
        with urllib.request.urlopen(request, timeout=4) as response:
            return response.status == 200
    except Exception:
        return False


@functools.cache
def has_chrome() -> bool:
    probe = (
        'import { chromium } from "playwright-core";'
        'for (const channel of ["chrome", "msedge", undefined]) {'
        "  try { const b = await chromium.launch({ channel, headless: true });"
        "        await b.close(); process.exit(0); } catch {}"
        "}"
        "process.exit(1);"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", probe],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.returncode == 0


def check_requirements(
    config: pytest.Config,
    *,
    keys: tuple[str, ...] = (),
    ollama: tuple[str, ...] = (),
    needs_local: bool = False,
    needs_internet: bool = False,
) -> None:
    if config.getoption("--offline") and (keys or ollama or needs_local or needs_internet):
        pytest.skip("skipped in --offline mode")

    missing_keys = [key for key in keys if not has_api_key(key)]
    if missing_keys:
        pytest.skip(f"needs {', '.join(missing_keys)} in .env")

    if ollama:
        available = ollama_models()
        if not available:
            pytest.skip("needs Ollama running on localhost:11434")
        missing_models = [m for m in ollama if m not in available]
        if missing_models:
            pytest.skip(f"needs Ollama model(s): {', '.join(missing_models)}")

    if needs_local and not has_local_extra():
        pytest.skip("needs optional local packages (`uv sync --extra local`)")

    if needs_internet and not has_internet():
        pytest.skip("needs internet access")


def verify_output_file(path: Path) -> None:
    assert path.is_file(), f"Expected output file was not written: {path}"
    content = path.read_text(encoding="utf-8")
    assert content.strip(), f"Output file is empty: {path}"

    if path.suffix == ".json":
        parsed = json.loads(content)
        assert parsed, f"JSON output file parsed to empty value: {path}"
    elif path.suffix == ".csv":
        lines = [line for line in content.splitlines() if line.strip()]
        assert len(lines) >= 2, f"CSV output file has no data rows: {path}"


def execute_python_script(
    script: Path,
    *,
    stdin: str | None = None,
    outputs: tuple[str, ...] = (),
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 240,
) -> subprocess.CompletedProcess[str]:
    output_dir = script.parent / "output"
    expected_paths = [output_dir / name for name in outputs]

    # Remove target output files beforehand so we know this run created them fresh.
    for target in expected_paths:
        target.unlink(missing_ok=True)

    # Default working directory is the module folder (or script parent if outside a module).
    if cwd is None:
        cwd = script.parent.parent if script.parent.name == "demo" else REPO_ROOT
        for parent in script.parents:
            if parent.name.startswith("module-"):
                cwd = parent
                break

    result = subprocess.run(
        [sys.executable, str(script)],
        input=stdin,
        cwd=cwd,
        env=clean_env() if env is None else env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    label = script.relative_to(REPO_ROOT) if script.is_relative_to(REPO_ROOT) else script
    assert result.returncode == 0, (
        f"{label} exited with code {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
    assert result.stdout.strip(), f"{label} printed nothing to stdout"

    for target in expected_paths:
        verify_output_file(target)

    return result
