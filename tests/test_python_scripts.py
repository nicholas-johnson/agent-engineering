"""Runs every standalone Python demo, playground, data builder, and clip script."""

from __future__ import annotations

import json
import re
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
    timeout: int = 240


INTRO = find_module("intro-to-language-models")
CHATBOT = find_module("building-a-chatbot")
TOOLS = find_module("tools")
PROVIDERS = find_module("choosing-a-provider")
EMBEDDINGS = find_module("embeddings-and-vector-search")
RAG = find_module("rag-and-proprietary-knowledge")
AI_DEV = find_module("ai-assisted-development")
SECURITY = find_module("security-and-deployment")

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
    # --- Embeddings and Vector Search ---
    ScriptCase(
        f"{EMBEDDINGS}/demo/01_keyword_search.py",
        outputs=("01_keyword_search.json",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/demo/04_similarity_search.py",
        outputs=("04_similarity_search.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/demo/05_vector_database.py",
        outputs=("05_vector_database.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/playground/word-vectors/play.py",
        stdin="boost\n\n",
        outputs=("closest.json", "vectors.txt"),
        slow=True,
    ),
    ScriptCase(
        f"{EMBEDDINGS}/playground/similarity-explorer/play.py",
        stdin="The heating works\nThe heating does not work\n\n\n",
        outputs=("similarities.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/playground/distance-measures/play.py",
        outputs=("results.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/playground/what-to-embed/play.py",
        outputs=("ranks.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/playground/other-languages/play.py",
        outputs=("ranks.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{EMBEDDINGS}/playground/shrink-the-vectors/play.py",
        outputs=("results.json",),
        keys=("OPENAI_API_KEY",),
    ),
    # --- RAG and Proprietary Knowledge ---
    ScriptCase(
        f"{RAG}/demo/01_just_ask.py",
        outputs=("01_just_ask.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{RAG}/demo/02_whole_manual.py",
        outputs=("02_whole_manual.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{RAG}/demo/03_retrieve_and_answer.py",
        outputs=("03_retrieve_and_answer.json", "chunks.json"),
        keys=("OPENAI_API_KEY",),
    ),
    # The first run embeds every chunk and question, which can take a few minutes.
    ScriptCase(
        f"{RAG}/demo/04_faq.py",
        outputs=("04_faq.json",),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    ScriptCase(
        f"{RAG}/demo/05_citations.py",
        outputs=("05_citations.json",),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    ScriptCase(
        f"{RAG}/demo/06_keep_it_current.py",
        outputs=("06_keep_it_current.json",),
        keys=("OPENAI_API_KEY",),
    ),
    # --- AI-Assisted Development ---
    ScriptCase(
        f"{AI_DEV}/demo/01_just_build_it.py",
        outputs=("01_prototype.html",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{AI_DEV}/demo/02_company_brain.py",
        outputs=("02_spec.md", "02_prototype.html"),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{AI_DEV}/demo/03_coding_agent.py",
        outputs=("03_changes.diff", "03_transcript.json"),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    ScriptCase(
        f"{AI_DEV}/demo/04_plan_first.py",
        stdin="y\n",
        outputs=("04_plan.md", "04_changes.diff", "04_transcript.json"),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    ScriptCase(
        f"{AI_DEV}/demo/05_skills.py",
        outputs=("05_review.md", "05_test-plan.md", "05_change-summary.md"),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{AI_DEV}/demo/06_out_the_door.py",
        outputs=("06_launch/release-notes.md", "06_launch/social-post.md", "06_launch/sales-sheet.md"),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{AI_DEV}/playground/brain-pieces/play.py",
        outputs=("nothing.txt", "product-decisions-design-voice.txt"),
        keys=("OPENAI_API_KEY",),
    ),
    # Says yes to every change the agent asks to make.
    ScriptCase(
        f"{AI_DEV}/playground/permissions/play.py",
        stdin="y\n" * 60,
        outputs=("changes.diff", "transcript.json"),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    ScriptCase(
        f"{AI_DEV}/playground/test-first/play.py",
        outputs=("tests.diff", "changes.diff", "transcript.json"),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    # The Claude review needs ANTHROPIC_API_KEY too, and is skipped without it.
    ScriptCase(
        f"{AI_DEV}/playground/second-opinion/play.py",
        outputs=("gpt-6-luna-none.md", "gpt-6-luna-high.md"),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    ScriptCase(
        f"{AI_DEV}/playground/write-a-skill/play.py",
        outputs=("support-reply.md",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{AI_DEV}/playground/feedback-themes/play.py",
        outputs=("themes.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{AI_DEV}/playground/voice-check/play.py",
        stdin="\n",
        outputs=("check.json",),
        keys=("OPENAI_API_KEY",),
    ),
    # --- Security and Commercial Deployment ---
    ScriptCase(
        f"{SECURITY}/demo/01_ship_it.py",
        outputs=("01_ship_it.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{SECURITY}/demo/02_access_control.py",
        outputs=("02_access_control.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{SECURITY}/demo/03_prompt_injection.py",
        outputs=("03_prompt_injection.json",),
        keys=("OPENAI_API_KEY",),
        timeout=600,
    ),
    # Declines the injected invitation, then allows the real one.
    ScriptCase(
        f"{SECURITY}/demo/04_guardrails.py",
        stdin="n\ny\n",
        outputs=("04_audit.jsonl",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{SECURITY}/demo/05_privacy.py",
        outputs=("05_log.jsonl",),
        keys=("OPENAI_API_KEY",),
    ),
    # Starts demo/06_dormouse_server.py twice, with Sam's token and Priya's.
    ScriptCase(
        f"{SECURITY}/demo/06_two_assistants.py",
        stdin="y\n",
        outputs=("06_two_assistants.json", "06_dormouse.json"),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{SECURITY}/playground/secret-keeper/play.py",
        stdin="\n",
        outputs=("attacks.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(
        f"{SECURITY}/playground/injection-lab/play.py",
        stdin="\n",
        outputs=("runs.json",),
        keys=("OPENAI_API_KEY",),
    ),
    ScriptCase(f"{SECURITY}/playground/who-sees-what/play.py", outputs=("results.json",)),
    ScriptCase(f"{SECURITY}/playground/redact/play.py", outputs=("redacted.json",)),
    ScriptCase(f"{SECURITY}/playground/lethal-trifecta/play.py", outputs=("report.json",)),
    ScriptCase(
        f"{SECURITY}/playground/spend-limits/play.py",
        outputs=("messages.json",),
        keys=("OPENAI_API_KEY",),
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
        # Demo 3 reads the word vectors demo 2 writes, so they run in order below.
        f"{EMBEDDINGS}/demo/02_word_vectors.py",
        f"{EMBEDDINGS}/demo/03_document_vectors.py",
        # Copies documents from Module 6: checked against them below instead.
        f"{EMBEDDINGS}/data/copy_docs.py",
        # Write the committed knowledge base and its FAQ with a model, so the same applies.
        f"{RAG}/data/build_docs.py",
        f"{RAG}/data/build_faq.py",
        # Copies documents from Module 6: checked against them below instead.
        f"{SECURITY}/data/build_kb.py",
        # The small codebase the coding agents change: its own unit tests run below.
        *(
            str(path.relative_to(REPO_ROOT))
            for path in sorted((REPO_ROOT / AI_DEV / "data" / "project").rglob("*.py"))
        ),
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
        timeout=case.timeout,
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


@pytest.mark.offline
def test_embeddings_data_is_consistent() -> None:
    """Module 5's documents are an exact copy of Module 6's, and every question's answers exist."""
    data = REPO_ROOT / EMBEDDINGS / "data"
    source = REPO_ROOT / RAG / "data" / "docs"
    docs = sorted((data / "docs").glob("*.md"))
    assert [p.name for p in docs] == sorted(p.name for p in source.glob("*.md"))
    for path in docs:
        assert path.read_text() == (source / path.name).read_text(), f"{path.name} differs from Module 6"
    audiences = [re.search(r"^audience: (\w+)$", p.read_text(), re.MULTILINE)[1] for p in docs]
    assert (audiences.count("customer"), audiences.count("internal")) == (234, 41)

    questions = json.loads((data / "questions.json").read_text(encoding="utf-8"))
    ids = {p.stem for p in docs}
    assert len(questions) == 20
    for question in questions:
        assert question["expected"], question["question"]
        assert set(question["expected"]) <= ids, question["question"]


@pytest.mark.api
@pytest.mark.slow
def test_word_vectors_then_document_vectors(pytestconfig: pytest.Config) -> None:
    """Demo 3 averages the word vectors demo 2 trains, so run them in order."""
    check_requirements(pytestconfig, keys=("OPENAI_API_KEY",))
    demo = REPO_ROOT / EMBEDDINGS / "demo"
    trained = execute_python_script(demo / "02_word_vectors.py", outputs=("02_word_vectors.txt",))
    assert "warm" in trained.stdout
    execute_python_script(demo / "03_document_vectors.py", outputs=("03_document_vectors.json",))


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


@pytest.mark.offline
def test_knowledge_base_is_consistent() -> None:
    """The documents have their fields, Warm Wake's details live in one place, and the questions can be answered."""
    module = REPO_ROOT / RAG / "data"
    documents = {path.name: path.read_text(encoding="utf-8") for path in sorted((module / "docs").glob("*.md"))}
    questions = json.loads((module / "questions.json").read_text(encoding="utf-8"))
    assert len(documents) > 250

    fields = ["title", "product", "type", "audience", "firmware", "updated"]
    for name, text in documents.items():
        assert text.isascii(), name
        front = text.split("---", 2)[1].strip().splitlines()
        assert [line.split(": ", 1)[0] for line in front] == fields, name
        assert f"audience: {'internal' if 'type: internal' in front else 'customer'}" in front, name

    # Firmware 4.2 changes Warm Wake, so only these documents may say how it works.
    for name, text in documents.items():
        if name not in {"user-guide.md", "firmware-4-0-release-notes.md"}:
            assert not re.search(r"minutes early|90 minutes|> Warm Wake", text, re.IGNORECASE), name

    def has(text: str, fact: str) -> bool:
        text = re.sub(r"\s*>\s*", ">", " ".join(text.lower().split()))
        return any(re.search(rf"\b{re.escape(option.lower())}\b", text) for option in fact.split("|"))

    guide = documents["user-guide.md"]
    for question in questions:
        if question["kind"] in ("everyday", "error code"):
            assert question["facts"], question["id"]
            assert all(has(guide, fact) for fact in question["facts"]), question["id"]

    # Only internal documents explain the relay click, so a customer answer that explains it has leaked one.
    holders = [name for name, text in documents.items() if "click" in text.lower()]
    assert holders and all("audience: internal" in documents[name] for name in holders)

    updates = sorted(path.name for path in (module / "updates").glob("*.md"))
    assert updates == ["release-notes-4.2.md", "user-guide.md"]

    # data/build_faq.py wrote questions for (nearly) every chunk, and each has some.
    faq = json.loads((module / "faq.json").read_text(encoding="utf-8"))
    assert len(faq) > 1700
    assert all(entry["questions"] and len(entry["checksum"]) == 64 for entry in faq.values())
    assert "user-guide.md#warm-wake" in faq


@pytest.mark.offline
def test_dormouse_project_tests_pass() -> None:
    """The codebase the coding agents start from must pass its own tests, or the demos mean nothing."""
    project = REPO_ROOT / AI_DEV / "data" / "project"
    result = subprocess.run(
        [sys.executable, "-m", "unittest"], cwd=project, capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    assert "Ran 16 tests" in result.stderr


@pytest.mark.offline
def test_ai_dev_data_is_consistent() -> None:
    """The skills load, the saved change applies to the project, and the ticket matches the feedback."""
    module = REPO_ROOT / AI_DEV / "data"
    for skill in sorted((module / "skills").glob("*/SKILL.md")):
        _, front, body = skill.read_text().split("---", 2)
        fields = dict(line.split(": ", 1) for line in front.strip().splitlines())
        assert fields["name"] == skill.parent.name
        assert fields["description"] and body.strip()
    for path in [*module.glob("brain/*.md"), *module.glob("skills/*/SKILL.md"), module / "tickets" / "DOR-231.md"]:
        assert path.read_text().isascii(), f"{path} is not plain ASCII"
    # The saved change must start from the committed project.
    diff = (module / "changes" / "DOR-231.diff").read_text()
    for removed in re.findall(r"^-(?!--)(.*)$", diff, re.MULTILINE):
        names = re.findall(r"^--- a/(\S+)", diff, re.MULTILINE)
        assert any(removed in (module / "project" / name).read_text() for name in names), removed
    feedback = json.loads((module / "feedback.json").read_text())
    assert len(feedback) == 30
    assert "14 of 30" in (module / "tickets" / "DOR-231.md").read_text()


@pytest.mark.offline
def test_security_data_is_consistent() -> None:
    """Module 8's knowledge base is an exact copy of part of Module 6's, and its attacks fit its data."""
    data = REPO_ROOT / SECURITY / "data"
    docs = REPO_ROOT / RAG / "data" / "docs"
    kb = sorted((data / "kb").glob("*.md"))
    for path in kb:
        assert path.read_text() == (docs / path.name).read_text(), f"{path.name} differs from Module 6"
    audiences = [re.search(r"^audience: (\w+)$", p.read_text(), re.MULTILINE)[1] for p in kb]
    assert (audiences.count("customer"), audiences.count("internal")) == (30, 12)
    dormouse = json.loads((data / "dormouse.json").read_text())
    attacks = json.loads((data / "attacks.json").read_text())
    devices = {d["id"] for home in dormouse["homes"] for d in home["devices"]}
    assert attacks["injection"]["device"] in devices
    for name in ("obvious", "helpful", "record"):
        assert attacks["injection"]["attacker_email"] in attacks["injection"][name]
    providers = json.loads((data / "providers.json").read_text())
    assert providers["checked_on"] and all(p["sources"] for p in providers["providers"])
