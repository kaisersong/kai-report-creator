"""Theme routing tests — the keyword table had no coverage at all.

`resolve_theme` is first-match-wins over `THEME_KEYWORDS` and matches substrings
across the whole IR, so row order *is* the contract. These tests pin the
precedence decisions that are easy to break by appending a row in the wrong
place, and mirror the table in `references/theme-routing.md`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from context_isolation import resolve_theme  # noqa: E402


def ir(title: str, body: str = "内容占位") -> str:
    return f"---\ntitle: {title}\n---\n\n## 概述\n\n{body}\n"


@pytest.mark.parametrize(
    "title,expected",
    [
        ("Q3 项目复盘", "forest-editorial"),
        ("2026 上半年工作总结", "forest-editorial"),
        ("阶段总结与后续计划", "forest-editorial"),
        ("新客获取方案", "forest-editorial"),
        ("组织调整提案", "forest-editorial"),
        ("Launch Retrospective", "forest-editorial"),
        ("Pricing Proposal", "forest-editorial"),
        ("米绿纸感风格报告", "forest-editorial"),
    ],
)
def test_retrospective_summary_and_proposal_route_to_forest_editorial(title, expected):
    assert resolve_theme(ir(title)) == expected


@pytest.mark.parametrize(
    "title,expected",
    [
        ("第 32 周周报", "regular-lumen"),          # explicit periodic wins
        ("7 月月报复盘", "regular-lumen"),          # ...even when it says 复盘
        ("Q3 季度业绩总结报告", "corporate-blue"),  # business signal wins
        ("支付网关技术方案", "dark-tech"),          # technical signal wins
        ("行业趋势回顾", "newspaper"),              # industry signal wins
    ],
)
def test_sharper_signals_outrank_forest_editorial(title, expected):
    assert resolve_theme(ir(title)) == expected


@pytest.mark.parametrize(
    "title,expected",
    [
        ("年度增长报告", "data-story"),
        ("Annual Growth Story", "data-story"),
    ],
)
def test_data_story_keeps_the_data_shaped_narrative(title, expected):
    assert resolve_theme(ir(title)) == expected


def test_bare_summary_section_does_not_hijack_the_theme():
    """A 总结 section is in almost every report; only compounds route."""
    assert resolve_theme(ir("支付成功率专项分析", "## 总结\n\n结论。")) == "corporate-blue"


def test_explicit_frontmatter_theme_still_wins():
    text = "---\ntitle: 项目复盘\ntheme: minimal\n---\n\n## 概述\n\n内容\n"
    assert resolve_theme(text) == "minimal"


def test_unmatched_text_falls_back_to_corporate_blue():
    assert resolve_theme(ir("门店排班安排")) == "corporate-blue"
