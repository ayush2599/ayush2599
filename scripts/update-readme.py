#!/usr/bin/env python3
"""Render profile.yml into README.md and the animated SVG header."""

from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path
from urllib.parse import quote

import yaml


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
HERO = ROOT / "assets" / "hero.svg"
PROFILE = ROOT / "data" / "profile.yml"


def replace_block(text: str, key: str, content: str) -> str:
    start = f"<!-- profile:{key}:start -->"
    end = f"<!-- profile:{key}:end -->"
    pattern = re.compile(rf"({re.escape(start)}).*?({re.escape(end)})", re.DOTALL)
    replacement = rf"\1\n{content.strip()}\n\2"
    updated, count = pattern.subn(replacement, text)
    if count != 1:
        raise ValueError(f"Expected exactly one marker block for {key!r}; found {count}.")
    return updated


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render_links(links: dict[str, str]) -> str:
    rendered = []
    for label, url in links.items():
        if url and "YOUR_" not in url:
            rendered.append(f'<a href="{html.escape(str(url), quote=True)}">{html.escape(str(label))}</a>')
    if not rendered:
        return "<!-- Add your real links in data/profile.yml; placeholders are intentionally hidden. -->"
    return '<p align="center">\n  ' + "\n  ·\n  ".join(rendered) + "\n</p>"


def replace_svg_field(svg: str, field: str, value: str) -> str:
    pattern = re.compile(
        rf'(<(?P<tag>text|tspan)\b[^>]*data-field="{re.escape(field)}"[^>]*>)'
        rf'.*?(</(?P=tag)>)'
    )
    escaped = html.escape(value, quote=False)
    updated, count = pattern.subn(lambda match: match.group(1) + escaped + match.group(3), svg)
    if count != 1:
        raise ValueError(f"Expected exactly one SVG field {field!r}; found {count}.")
    return updated


def main() -> None:
    profile = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")

    focus = "\n".join(f"- {md_cell(item)}" for item in profile["current_focus"])
    building_rows = "\n".join(
        f'| {md_cell(item["name"])} | {md_cell(item["purpose"])} | `{md_cell(item["state"])}` |'
        for item in profile["currently_building"]
    )
    building = "| Project | What it is solving | State |\n|---|---|---|\n" + building_rows
    skill_rows = "\n".join(
        f"| **{md_cell(capability)}** | {md_cell(tools)} |"
        for capability, tools in profile["capabilities"].items()
    )
    skills = "| Capability | Tools and territory |\n|---|---|\n" + skill_rows

    jokes = profile.get("jokes") or ["Good systems make the hard things boring."]
    joke = jokes[dt.date.today().toordinal() % len(jokes)]

    for key, content in {
        "about": profile["about"],
        "focus": focus,
        "building": building,
        "skills": skills,
        "outside": profile["outside_the_terminal"],
        "joke": f"> “{joke}”",
        "links": render_links(profile.get("links", {})),
    }.items():
        readme = replace_block(readme, key, content)

    username = str(profile["github_username"]).strip()
    readme = re.sub(
        r"raw\.githubusercontent\.com/[^/]+/[^/]+/output/",
        f"raw.githubusercontent.com/{quote(username)}/{quote(username)}/output/",
        readme,
    )
    README.write_text(readme.rstrip() + "\n", encoding="utf-8")

    svg = HERO.read_text(encoding="utf-8")
    first_focus = str(profile["current_focus"][0])[:43]
    for field, value in {
        "name": str(profile["name"])[:32],
        "headline": str(profile["headline"])[:58],
        "focus": first_focus,
        "status": str(profile["status"]).upper()[:30],
    }.items():
        svg = replace_svg_field(svg, field, value)
    HERO.write_text(svg, encoding="utf-8")

    print("Updated README.md and assets/hero.svg from data/profile.yml")


if __name__ == "__main__":
    main()
