"""Runs every standalone Python demo, playground, data builder, and clip script."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from tests.conftest import (
    API_KEYS,
    REPO_ROOT,
    check_requirements,
    clean_env,
    execute_python_script,
    find_module,
    has_api_key,
    verify_output_file,
)


@dataclass(frozen=True)
class ScriptCase:
    path: str
    outputs: tuple[str, ...] = ()
    stdin: str | None = None
    keys: tuple[str, ...] = ()
    ollama: tuple[str, ...] = ()
    needs_local: bool = False
    needs_internet: bool = False
    slow: bool = False


INTRO = find_module("intro-to-language-models")
CHATBOT = find_module("building-a-chatbot")
TOOLS = find_module("tools")
PROVIDERS = find_module("choosing-a-provider")

SCRIPTS: tuple[ScriptCase, ...] = (
    # --- Intro to Language Models (all offline) ---
    ScriptCase(
        f"{INTRO}/demo/01_word_pairs.py",
        outputs=("01_word_pairs_alice-chapter-1.json", "01_word_pairs_alice.json"),
    ),
    ScriptCase(
        f"{INTRO}/demo/02_context_window.py",
        outputs=("02_context_window_alice-chapter-1.json", "02_context_window_alice.json"),
    ),
    ScriptCase(
        f"{INTRO}/demo/03_letters.py",
        outputs=("03_letters_alice-chapter-1.json", "03_letters_alice.json"),
    ),
    ScriptCase(
        f"{INTRO}/demo/04_tokens.py",
        outputs=("04_tokens_alice-chapter-1.json", "04_tokens_alice.json"),
    ),
    ScriptCase(
        f"{INTRO}/demo/05_neural_model.py",
        outputs=("05_neural_model_embeddings.txt",),
        slow=True,
    ),
    ScriptCase(
        f"{INTRO}/playground/finish-my-sentence/play.py",
        stdin="alice was beginning to get\n\n",
    ),
    ScriptCase(
        f"{INTRO}/playground/temperature/play.py",
        outputs=("after_the.json",),
    ),
    ScriptCase(
        f"{INTRO}/playground/backoff/play.py",
        outputs=("backoff_counts.json",),
    ),
    ScriptCase(
        f"{INTRO}/playground/score-a-sentence/play.py",
        outputs=("scores.txt",),
    ),
    ScriptCase(
        f"{INTRO}/playground/other-books/play.py",
        outputs=("alice.txt", "looking-glass.txt", "python.txt"),
    ),
    ScriptCase(
        f"{INTRO}/playground/tokenizer-lab/play.py",
        outputs=("tokens_100.json", "tokens_500.json", "tokens_2000.json"),
        slow=True,
    ),
    # --- Building a Chatbot ---
    ScriptCase(
        f"{CHATBOT}/demo/01_one_response.py",
        outputs=("01_response.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/demo/02_chat_loop.py",
        stdin="Hello!\n\n",
        outputs=("02_chat_loop.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/demo/03_conversation.py",
        stdin="My name is Alice.\nWhat is my name?\n\n",
        outputs=("03_conversation.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/demo/04_streaming.py",
        stdin="Hello!\n\n",
        outputs=("04_streaming.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/demo/05_images.py",
        stdin="\n",
        outputs=("05_images.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/chatbot/play.py",
        stdin="Hello!\n\n",
        outputs=("conversation.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/personas/play.py",
        stdin="1\nHello!\n\n",
        outputs=("cheshire-cat.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/temperature/play.py",
        outputs=("temperatures.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/model-shootout/play.py",
        outputs=("shootout.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/cost-of-memory/play.py",
        outputs=("tokens_per_turn.csv",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/logprobs/play.py",
        outputs=("logprobs.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{CHATBOT}/playground/vision/play.py",
        outputs=("descriptions.txt",),
        keys=("OPENAI_API_KEY",),
    ),
    # --- Tools ---
    ScriptCase(
        f"{TOOLS}/demo/01_maths.py",
        outputs=("01_maths.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{TOOLS}/demo/02_function.py",
        outputs=("02_function.txt",),
    ),
    ScriptCase(
        f"{TOOLS}/demo/03_agent.py",
        outputs=("03_agent.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{TOOLS}/demo/04_agent.py",
        outputs=("04_agent.json",),
        keys=("OPENAI_API_KEY",),
        needs_internet=True,
    ),
    ScriptCase(
        f"{TOOLS}/playground/calculator/play.py",
        outputs=("conversations.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{TOOLS}/playground/tool-descriptions/play.py",
        outputs=("results.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{TOOLS}/playground/raw-protocol/play.py",
        outputs=("messages.json",),
    ),
    ScriptCase(
        f"{TOOLS}/playground/lying-tools/play.py",
        outputs=("results.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{TOOLS}/playground/parallel-calls/play.py",
        outputs=("conversation.json",),
        keys=("OPENAI_API_KEY",),
        needs_internet=True,
    ),
    ScriptCase(
        f"{TOOLS}/playground/weather-server/play.py",
        outputs=("conversation.json",),
        keys=("OPENAI_API_KEY",),
        needs_internet=True,
    ),
    # --- Choosing a Provider ---
    ScriptCase(
        f"{PROVIDERS}/demo/02_one_key.py",
        outputs=("02_one_key.json",),
        keys=("OPENROUTER_API_KEY",),
    ),
    ScriptCase(
        f"{PROVIDERS}/demo/03_chinese_labs.py",
        outputs=("03_chinese_labs.json",),
        keys=("OPENROUTER_API_KEY",),
    ),
    ScriptCase(
        f"{PROVIDERS}/demo/04_ollama.py",
        outputs=("04_ollama.txt",),
        ollama=("qwen3:1.7b",),
    ),
    ScriptCase(
        f"{PROVIDERS}/demo/05_python.py",
        outputs=("05_python.json",),
        needs_local=True,
    ),
    ScriptCase(
        f"{PROVIDERS}/demo/06_choosing.py",
        outputs=("06_scorecard.json",),
        ollama=("qwen3:1.7b",),
    ),
    ScriptCase(
        f"{PROVIDERS}/playground/price-calculator/play.py",
        outputs=("monthly_costs.csv",),
    ),
    ScriptCase(
        f"{PROVIDERS}/playground/model-catalogue/play.py",
        outputs=("catalogue.json",),
        needs_internet=True,
    ),
    ScriptCase(
        f"{PROVIDERS}/playground/local-models/play.py",
        outputs=("answers.txt",),
        ollama=("qwen3:0.6b", "qwen3:1.7b"),
    ),
    ScriptCase(
        f"{PROVIDERS}/playground/open-vs-closed/play.py",
        outputs=("answers.json",),
        keys=("OPENAI_API_KEY",),
        ollama=("qwen3:1.7b",),
    ),
    ScriptCase(
        f"{PROVIDERS}/playground/content-policies/play.py",
        outputs=("answers.json",),
        ollama=("qwen3:1.7b",),
    ),
    ScriptCase(
        f"{PROVIDERS}/playground/your-own-loop/play.py",
        outputs=("steps.json",),
        needs_local=True,
    ),
    # --- Social clip companion script ---
    ScriptCase("social-scripts/02-how-ai-learns/neuron.py"),
)

# Scripts handled by dedicated multi-step or isolated-directory tests below.
DEDICATED_SCRIPTS: frozenset[str] = frozenset(
    {
        f"{INTRO}/data/build_tokens.py",
        f"{INTRO}/playground/neural-knobs/train.py",
        f"{INTRO}/playground/neural-knobs/complete.py",
        f"{PROVIDERS}/data/build_prices.py",
        f"{PROVIDERS}/demo/01_big_labs.py",
    }
)

COVERED_SCRIPTS: frozenset[str] = frozenset(c.path for c in SCRIPTS) | DEDICATED_SCRIPTS


def _marks_for(case: ScriptCase) -> list[pytest.MarkDecorator]:
    marks: list[pytest.MarkDecorator] = []
    if case.keys:
        marks.append(pytest.mark.api)
    if case.ollama:
        marks.append(pytest.mark.ollama)
    if case.needs_local:
        marks.append(pytest.mark.local)
    if case.needs_internet:
        marks.append(pytest.mark.network)
    if not marks:
        marks.append(pytest.mark.offline)
    if case.slow:
        marks.append(pytest.mark.slow)
    return marks


@pytest.mark.parametrize(
    "case",
    [pytest.param(case, id=case.path, marks=_marks_for(case)) for case in SCRIPTS],
)
def test_script(case: ScriptCase, pytestconfig: pytest.Config) -> None:
    check_requirements(
        pytestconfig,
        keys=case.keys,
        ollama=case.ollama,
        needs_local=case.needs_local,
        needs_internet=case.needs_internet,
    )
    execute_python_script(
        REPO_ROOT / case.path,
        stdin=case.stdin,
        outputs=case.outputs,
    )


@pytest.mark.offline
@pytest.mark.slow
def test_neural_knobs_train_and_complete() -> None:
    """complete.py loads output/model.json produced by train.py, so run them in order."""
    folder = REPO_ROOT / INTRO / "playground" / "neural-knobs"
    execute_python_script(folder / "train.py", outputs=("model.json",))
    result = execute_python_script(
        folder / "complete.py",
        stdin="alice was beginning to get\n\n",
    )
    assert "alice" in result.stdout.lower()


@pytest.mark.offline
def test_build_tokens_matches_committed_data(tmp_path: Path) -> None:
    """Run build_tokens.py in tmp_path so committed data/tokens.json is never modified."""
    data_dir = REPO_ROOT / INTRO / "data"
    shutil.copy2(data_dir / "build_tokens.py", tmp_path / "build_tokens.py")
    shutil.copy2(data_dir / "alice.txt", tmp_path / "alice.txt")

    execute_python_script(tmp_path / "build_tokens.py", cwd=tmp_path)

    generated = json.loads((tmp_path / "tokens.json").read_text(encoding="utf-8"))
    committed = json.loads((data_dir / "tokens.json").read_text(encoding="utf-8"))
    assert len(generated) == 500
    assert generated == committed


@pytest.mark.network
def test_build_prices(tmp_path: Path, pytestconfig: pytest.Config) -> None:
    """Run build_prices.py in tmp_path to verify every listed model still exists on OpenRouter."""
    check_requirements(pytestconfig, needs_internet=True)
    data_dir = REPO_ROOT / PROVIDERS / "data"
    shutil.copy2(data_dir / "build_prices.py", tmp_path / "build_prices.py")

    execute_python_script(tmp_path / "build_prices.py", cwd=tmp_path)
    verify_output_file(tmp_path / "prices.json")

    prices = json.loads((tmp_path / "prices.json").read_text(encoding="utf-8"))
    assert len(prices["models"]) > 0


@pytest.mark.offline
def test_big_labs_graceful_skip_without_keys(tmp_path: Path) -> None:
    """01_big_labs.py should skip missing provider keys cleanly rather than crashing."""
    # Run from an empty temp cwd with keys stripped so load_dotenv() will not find repo .env.
    script = REPO_ROOT / PROVIDERS / "demo" / "01_big_labs.py"
    result = execute_python_script(
        script,
        outputs=("01_big_labs.json",),
        cwd=tmp_path,
        env=clean_env(strip_keys=True),
    )
    assert "skipped: no OPENAI_API_KEY" in result.stdout


@pytest.mark.api
def test_big_labs_live(pytestconfig: pytest.Config) -> None:
    """Run 01_big_labs.py against whichever frontier lab keys are configured in .env."""
    if pytestconfig.getoption("--offline"):
        pytest.skip("skipped in --offline mode")
    lab_keys = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "XAI_API_KEY")
    if not any(has_api_key(key) for key in lab_keys):
        pytest.skip(f"needs at least one of {', '.join(lab_keys)} in .env")

    script = REPO_ROOT / PROVIDERS / "demo" / "01_big_labs.py"
    execute_python_script(script, outputs=("01_big_labs.json",))
    answers = json.loads((script.parent / "output" / "01_big_labs.json").read_text(encoding="utf-8"))
    assert any(not text.startswith("(skipped:") for text in answers.values())


@pytest.mark.offline
@pytest.mark.parametrize(
    "rel_path",
    [
        f"{PROVIDERS}/demo/02_one_key.py",
        f"{PROVIDERS}/demo/03_chinese_labs.py",
    ],
)
def test_openrouter_demos_exit_cleanly_without_key(rel_path: str, tmp_path: Path) -> None:
    """Demos requiring OPENROUTER_API_KEY should exit with a clear message, not a traceback."""
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / rel_path)],
        cwd=tmp_path,
        env={k: v for k, v in clean_env(strip_keys=True).items() if k not in API_KEYS},
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode != 0
    assert "OPENROUTER_API_KEY" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.offline
def test_demos_run_from_any_working_directory(tmp_path: Path) -> None:
    """MODULE_GUIDE.md requires demos to resolve paths via Path(__file__).parent."""
    script = REPO_ROOT / INTRO / "demo" / "01_word_pairs.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        env=clean_env(),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert "=== alice ===" in result.stdout
