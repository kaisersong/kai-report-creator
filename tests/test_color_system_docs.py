from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_corporate_blue_theme_uses_warm_business_tokens():
    src = read("templates/themes/corporate-blue.css")
    assert "--bg: #F8F5EF;" in src
    assert "--surface: #FFFDF9;" in src
    assert "--text: #2B2623;" in src
    assert "--primary: #1F6F50;" in src
    assert "--accent: #C79A2B;" in src
    assert "--border: #E7DDD2;" in src


def test_design_quality_business_hint_matches_new_default_direction():
    src = read("references/design-quality.md")
    assert "| **Business / Data** | 销售、营收、KPI、增长、季报、业绩 / sales, revenue, KPI, growth, quarterly | `#1F6F50` (pine green) | Restrained, commercial, premium |" in src
