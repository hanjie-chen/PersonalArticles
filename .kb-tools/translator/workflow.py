from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


BRIEF_INTRO_PATTERN = re.compile(r"```.*?BriefIntroduction:\s*(.*?)```", re.DOTALL)
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SOURCE_BLOB_PATTERN = re.compile(r"<!--\s*source_blob:\s*([0-9a-f]{40})\s*-->")
REQUIRED_FRONTMATTER_FIELDS = ("Title", "Author", "CoverImage", "RolloutDate")


@dataclass(frozen=True)
class Candidate:
    source_md: Path
    status: str


def default_repo_root(script_path: Path) -> Path:
    current = script_path.resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if candidate.name == ".kb-tools":
            return candidate.parent

    return script_path.resolve().parent.parent


def resolve_codex_command() -> str:
    for candidate in ("codex", "codex.cmd", "codex.exe"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise RuntimeError("Could not find Codex CLI on PATH")


def is_hidden_item(item_name: str) -> bool:
    return item_name.startswith(".") or (
        item_name.startswith("__") and item_name.endswith("__")
    )


def is_scannable_directory(path: Path, root_dir: Path) -> bool:
    try:
        relative_parts = path.relative_to(root_dir).parts
    except ValueError:
        return False
    return not any(is_hidden_item(part) for part in relative_parts)


def extract_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return None

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def is_publishable_markdown(md_path: Path) -> bool:
    text = md_path.read_text(encoding="utf-8")
    if "<!-- split -->" not in text:
        return False

    metadata_part = text.split("<!-- split -->", 1)[0]
    metadata = extract_frontmatter(metadata_part)
    if not metadata:
        return False

    if not BRIEF_INTRO_PATTERN.search(metadata_part):
        return False

    return all(metadata.get(field) for field in REQUIRED_FRONTMATTER_FIELDS)


def compute_source_blob(root_dir: Path, source_md: Path) -> str:
    result = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={root_dir}",
            "-C",
            str(root_dir),
            "hash-object",
            str(source_md),
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def read_translation_source_blob(translation_md: Path) -> str | None:
    if not translation_md.exists():
        return None

    text = translation_md.read_text(encoding="utf-8")
    match = SOURCE_BLOB_PATTERN.search(text)
    if not match:
        return None
    return match.group(1)


def expected_translation_path(source_md: Path) -> Path:
    return source_md.parent / "resources" / "i18n" / f"{source_md.stem}-en.md"


def extract_translation_source(source_md: Path) -> str:
    text = source_md.read_text(encoding="utf-8")
    divided_article = text.split("<!-- split -->", 1)
    if len(divided_article) != 2:
        raise ValueError(f"{source_md} is not publishable")
    return divided_article[1].lstrip("\n")


def cover_image_path(source_md: Path) -> str | None:
    text = source_md.read_text(encoding="utf-8")
    metadata_part = text.split("<!-- split -->", 1)[0]
    metadata = extract_frontmatter(metadata_part)
    if not metadata:
        return None
    cover_image = metadata.get("CoverImage")
    return cover_image.strip() if cover_image else None


def remove_leading_cover_image(translated_markdown: str, cover_image: str | None) -> str:
    if not cover_image:
        return translated_markdown

    lines = translated_markdown.splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines):
        return translated_markdown

    line = lines[index].strip()
    is_cover_html = line.startswith("<img") and cover_image in line
    is_cover_markdown = line.startswith("![") and f"({cover_image})" in line
    if not (is_cover_html or is_cover_markdown):
        return translated_markdown

    remaining_lines = lines[:index] + lines[index + 1 :]
    while remaining_lines and not remaining_lines[0].strip():
        remaining_lines.pop(0)
    return "\n".join(remaining_lines).rstrip() + "\n"


def find_candidates(root_dir: Path, limit: int | None = 1) -> list[Candidate]:
    candidates: list[Candidate] = []

    for current_dir in sorted(root_dir.rglob("*")):
        if limit is not None and len(candidates) >= limit:
            break
        if not current_dir.is_dir() or not is_scannable_directory(current_dir, root_dir):
            continue
        if not (current_dir / "resources" / "images").is_dir():
            continue

        for source_md in sorted(current_dir.glob("*.md")):
            if limit is not None and len(candidates) >= limit:
                break
            if not is_publishable_markdown(source_md):
                continue

            translation_md = expected_translation_path(source_md)
            if not translation_md.exists():
                candidates.append(
                    Candidate(source_md=source_md, status="missing_translation")
                )
                continue

            source_blob = compute_source_blob(root_dir, source_md)
            translation_blob = read_translation_source_blob(translation_md)
            if translation_blob != source_blob:
                candidates.append(
                    Candidate(source_md=source_md, status="outdated_translation")
                )

    return candidates


def request_translation(
    *,
    repo_root: Path,
    source_markdown: str,
    model: str | None,
) -> str:
    prompt = (
        "Translate the following Markdown article body from Simplified Chinese to English.\n"
        "Requirements:\n"
        "- Keep the Markdown structure intact.\n"
        "- Translate headings and prose naturally into clear English.\n"
        "- Preserve code fences, code content, inline code, links, image paths, and HTML tags unless natural-language alt text needs translation.\n"
        "- Do not add frontmatter.\n"
        "- Return only the translated Markdown body.\n\n"
        "Markdown body:\n"
        f"{source_markdown}"
    )

    with tempfile.NamedTemporaryFile(
        "w+", encoding="utf-8", delete=False, suffix=".md"
    ) as temp_output:
        output_path = Path(temp_output.name)

    command = [
        resolve_codex_command(),
        "exec",
        "-C",
        str(repo_root),
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
    ]
    if model:
        command.extend(["--model", model])
    command.extend(
        [
            "-o",
            str(output_path),
        ]
    )

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=True,
            text=False,
            input=prompt.encode("utf-8"),
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise RuntimeError(
            f"Codex translation request failed: {stderr or stdout or exc}"
        ) from exc

    translated = output_path.read_text(encoding="utf-8").strip()
    output_path.unlink(missing_ok=True)
    if not translated:
        stderr = (result.stderr or b"").decode("utf-8", errors="replace").strip()
        raise RuntimeError(
            f"Codex translation request did not produce text output: {stderr}"
        )
    return translated + "\n"


def write_translation_file(
    translation_md: Path, source_blob: str, translated_markdown: str
) -> None:
    translation_md.parent.mkdir(parents=True, exist_ok=True)
    content = f"<!-- source_blob: {source_blob} -->\n\n{translated_markdown.lstrip()}"
    translation_md.write_text(content, encoding="utf-8")


def translate_candidate(
    *,
    repo_root: Path,
    candidate: Candidate,
    model: str | None,
) -> Path:
    source_blob = compute_source_blob(repo_root, candidate.source_md)
    source_markdown = extract_translation_source(candidate.source_md)
    cover_image = cover_image_path(candidate.source_md)
    translated_markdown = request_translation(
        repo_root=repo_root,
        source_markdown=source_markdown,
        model=model,
    )
    translated_markdown = remove_leading_cover_image(translated_markdown, cover_image)
    translation_md = expected_translation_path(candidate.source_md)
    write_translation_file(translation_md, source_blob, translated_markdown)
    return translation_md

