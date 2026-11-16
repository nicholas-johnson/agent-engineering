"""Verifies slide-deck linting, Prettier formatting, slide data validity, and Vite builds."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

from tests.conftest import REPO_ROOT

VALID_SLIDE_TYPES = {
    None,
    "standard",
    "title",
    "comparison",
    "three-way",
    "code",
    "rules",
    "welcome",
    "modules",
    "image",
    "equation",
    "cards",
    "description",
    "network",
    "tool-loop",
    "custom",
}


def _discover_slide_decks() -> list[tuple[str, Path, str]]:
    decks: list[tuple[str, Path, str]] = []
    for pkg_json in sorted(REPO_ROOT.glob("day-*/module-*/slides/package.json")):
        slides_dir = pkg_json.parent
        module_name = slides_dir.parent.name
        pkg_name = json.loads(pkg_json.read_text(encoding="utf-8"))["name"]
        decks.append((module_name, slides_dir, pkg_name))
    return decks


def _available_icons() -> set[str]:
    source = (REPO_ROOT / "slide-deck/src/components/SlideIcon.jsx").read_text(encoding="utf-8")
    block = re.search(r"const iconMap\s*=\s*\{(.*?)\n\};", source, flags=re.DOTALL)
    assert block, "Could not locate iconMap in SlideIcon.jsx"
    return {
        match.group(1) or match.group(2)
        for match in re.finditer(r"^\s*(?:'([^']+)'|([A-Za-z0-9_-]+))\s*:", block.group(1), re.M)
    }


def _collect_icons(obj: object) -> list[str]:
    found: list[str] = []
    if isinstance(obj, dict):
        if isinstance(obj.get("icon"), str):
            found.append(obj["icon"])
        for value in obj.values():
            found.extend(_collect_icons(value))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_collect_icons(item))
    return found


def _has_emoji_key(obj: object) -> bool:
    if isinstance(obj, dict):
        if "emoji" in obj:
            return True
        return any(_has_emoji_key(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_emoji_key(item) for item in obj)
    return False


SLIDE_DECKS = _discover_slide_decks()


@pytest.mark.offline
@pytest.mark.slides
def test_eslint_slide_deck() -> None:
    result = subprocess.run(
        ["pnpm", "lint:slides"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"pnpm lint:slides failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.offline
@pytest.mark.slides
def test_prettier_module_slides() -> None:
    result = subprocess.run(
        [
            "pnpm",
            "exec",
            "prettier",
            "--check",
            "day-*/module-*/slides/src/**",
            "day-*/closing/slides/src/**",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"Prettier formatting check failed on module slides:\n{result.stdout}\n{result.stderr}"
    )


@pytest.mark.offline
@pytest.mark.slides
@pytest.mark.parametrize(
    "module_name,slides_dir,pkg_name",
    SLIDE_DECKS,
    ids=[m for m, _, _ in SLIDE_DECKS],
)
def test_slides_schema_and_icons(module_name: str, slides_dir: Path, pkg_name: str) -> None:
    number = module_name.split("-")[1]
    assert pkg_name == f"@agent-engineering/module-{number}-slides", (
        f"{slides_dir}/package.json name {pkg_name!r} does not match folder {module_name!r}"
    )

    slides_js = slides_dir / "src" / "slides.js"
    loader = (
        f'const mod = await import({json.dumps(slides_js.as_uri())});'
        "const slides = mod.default ?? mod.slides;"
        "console.log(JSON.stringify(slides));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", loader],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"Could not load {slides_js}:\n{result.stderr}"

    slides = json.loads(result.stdout)
    assert isinstance(slides, list) and len(slides) >= 5, f"{module_name} has too few slides"

    valid_icons = _available_icons()
    for idx, slide in enumerate(slides, start=1):
        slide_type = slide.get("type")
        assert slide_type in VALID_SLIDE_TYPES, (
            f"{module_name} slide {idx} has unknown type {slide_type!r}"
        )
        assert not _has_emoji_key(slide), (
            f"{module_name} slide {idx} uses 'emoji'; MODULE_GUIDE.md requires 'icon'"
        )
        for icon in _collect_icons(slide):
            assert icon.lower() in valid_icons, (
                f"{module_name} slide {idx} uses unknown icon {icon!r} (not in SlideIcon.jsx)"
            )


@pytest.mark.offline
@pytest.mark.slides
@pytest.mark.parametrize(
    "module_name,slides_dir,pkg_name",
    SLIDE_DECKS,
    ids=[m for m, _, _ in SLIDE_DECKS],
)
def test_slides_vite_build(
    module_name: str, slides_dir: Path, pkg_name: str, tmp_path: Path
) -> None:
    """Build each deck into tmp_path so no dist/ folder is left inside the repository."""
    out_dir = tmp_path / module_name
    result = subprocess.run(
        [
            "pnpm",
            "--dir",
            str(slides_dir),
            "exec",
            "vite",
            "build",
            "--outDir",
            str(out_dir),
            "--emptyOutDir",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"Vite build failed for {pkg_name}:\n{result.stdout}\n{result.stderr}"
    )
    assert (out_dir / "index.html").is_file()
    assert not (slides_dir / "dist").exists(), f"Build leaked dist/ into {slides_dir}"
