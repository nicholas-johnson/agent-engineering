"""Verifies social promo clips in social-scripts/."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tests.conftest import REPO_ROOT, has_chrome

SOCIAL_DIR = REPO_ROOT / "social-scripts"


def _discover_clips() -> list[Path]:
    if not SOCIAL_DIR.is_dir():
        return []
    return sorted(
        entry
        for entry in SOCIAL_DIR.iterdir()
        if entry.is_dir() and (entry / "index.html").is_file()
    )


CLIPS = _discover_clips()


@pytest.mark.offline
@pytest.mark.clips
@pytest.mark.parametrize("clip_dir", CLIPS, ids=[c.name for c in CLIPS])
def test_clip_files_exist(clip_dir: Path) -> None:
    assert (clip_dir / "index.html").read_text(encoding="utf-8").strip()
    assert (clip_dir / "script.md").is_file(), f"{clip_dir.name} is missing script.md"
    assert (clip_dir / "script.md").read_text(encoding="utf-8").strip()


@pytest.mark.clips
@pytest.mark.parametrize("clip_dir", CLIPS, ids=[c.name for c in CLIPS])
def test_clip_deck_check(clip_dir: Path) -> None:
    if not has_chrome():
        pytest.skip("headless Chrome is not available for clip-deck check")

    output_root = SOCIAL_DIR / "output"
    had_output_root = output_root.exists()
    had_clip_output = (output_root / clip_dir.name).exists()

    try:
        result = subprocess.run(
            ["pnpm", "social:check", clip_dir.name],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, (
            f"pnpm social:check {clip_dir.name} reported problems:\n"
            f"{result.stdout}\n{result.stderr}"
        )
        assert "No problems found." in result.stdout
    finally:
        if not had_clip_output and (output_root / clip_dir.name).exists():
            shutil.rmtree(output_root / clip_dir.name, ignore_errors=True)
        if not had_output_root and output_root.exists():
            try:
                output_root.rmdir()
            except OSError:
                pass
