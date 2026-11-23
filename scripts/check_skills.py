#!/usr/bin/env python3
"""Check the format of the skills in skills/.

For each skills/<name>/:
- SKILL.md exists and starts with a YAML header with `name` (equal to the
  folder name) and `description`;
- SKILL.md is not longer than 500 lines (move detail to a subfolder);
- if there is a versions/ folder, its files are named like 20.0.md, and every
  versions/<N>.md that SKILL.md mentions exists;
- every relative markdown link in the skill points to a file that exists, and
  to a heading that exists when it has an #anchor.

Usage: check_skills.py [--root DIR]
Exit code 0 when everything is fine, 1 otherwise.
"""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE_RE = re.compile(r"^\d+\.\d+\.md$")
VERSION_MENTION_RE = re.compile(r"versions/(\d+\.\d+\.md)")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
MAX_SKILL_LINES = 500


def frontmatter(text):
    """(name, has_description) from the YAML header, or None if missing."""
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        return None
    name = re.search(r"^name:\s*(\S+)", match.group(1), re.M)
    has_description = bool(re.search(r"^description:", match.group(1), re.M))
    return (name.group(1) if name else None), has_description


def outside_fences(text):
    """The lines of a markdown text that are not inside a code fence."""
    lines, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            lines.append(line)
    return lines


def slug(heading):
    """The anchor GitHub gives to a heading."""
    text = heading.strip().lower().replace("`", "")
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path):
    found = set()
    for line in outside_fences(path.read_text(encoding="utf-8")):
        match = re.match(r"#{1,6}\s+(.*?)\s*$", line)
        if match:
            found.add(slug(match.group(1)))
    return found


def check_links(directory):
    errors = []
    for md in sorted(directory.rglob("*.md")):
        label = md.relative_to(directory.parent)
        text = "\n".join(outside_fences(md.read_text(encoding="utf-8")))
        for target in LINK_RE.findall(text):
            if re.match(r"[a-z][a-z0-9+.-]*:", target):
                continue
            name, _, fragment = target.partition("#")
            destination = (md.parent / name) if name else md
            if not destination.is_file():
                errors.append(f"{label}: link to {target} but {name} "
                              "does not exist")
            elif fragment and fragment not in anchors(destination):
                errors.append(f"{label}: link to {target} but that file has "
                              f"no heading #{fragment}")
    return errors


def check_skill(directory):
    folder = directory.name
    skill_md = directory / "SKILL.md"
    if not skill_md.is_file():
        return [f"{folder}: SKILL.md not found"]
    text = skill_md.read_text(encoding="utf-8")
    errors = []
    header = frontmatter(text)
    if header is None:
        return [f"{folder}: SKILL.md has no frontmatter"]
    name, has_description = header
    if name != folder:
        errors.append(f"{folder}: frontmatter name is '{name}'")
    if not has_description:
        errors.append(f"{folder}: frontmatter has no description")
    lines = len(text.splitlines())
    if lines > MAX_SKILL_LINES:
        errors.append(f"{folder}: SKILL.md has {lines} lines "
                      f"(max {MAX_SKILL_LINES}); move detail to a subfolder")
    versions = directory / "versions"
    if versions.is_dir():
        for path in sorted(versions.iterdir()):
            if not VERSION_FILE_RE.match(path.name):
                errors.append(f"{folder}: versions/{path.name} is not named "
                              "like 20.0.md")
    for mentioned in sorted(set(VERSION_MENTION_RE.findall(text))):
        if not (versions / mentioned).is_file():
            errors.append(f"{folder}: SKILL.md mentions versions/{mentioned}, "
                          "which does not exist")
    errors += check_links(directory)
    return errors


def check(root):
    skills = root / "skills"
    directories = sorted(p for p in skills.iterdir() if p.is_dir())
    errors = []
    for directory in directories:
        errors += check_skill(directory)
    return errors, len(directories)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)
    errors, count = check(args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {count} skill(s) checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
