#!/usr/bin/env python3
"""Validate final HTML report quality gates.

This complements guard_validate.py, which validates IR before rendering.
html_quality_gate.py validates the final HTML shell, theme fidelity, and KPI
rendering so direct HTML generation cannot bypass the guardrails.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import html as html_lib
import json
import re
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\[(?:INSERT VALUE|数据待填写)\]")

STANDARD_REQUIRED_IDS = [
    "report-summary",
    "toc-toggle-btn",
    "toc-sidebar",
    "card-mode-btn",
    "sc-overlay",
    "edit-hotzone",
    "edit-toggle",
    "export-btn",
    "export-menu",
    "export-print",
    "export-png-desktop",
    "export-png-mobile",
    "export-im-share",
]

ANIMATED_MODES = ("scrollytelling", "iridescence")

ANIMATED_ALLOWED_SCRIPT_HOSTS = ("https://cdnjs.cloudflare.com/",)

FORBIDDEN_FONT_ORIGINS = ("fonts.googleapis.com", "fonts.gstatic.com")


def is_animated_html(html: str) -> bool:
    return bool(re.search(r'data-render-mode=["\']animated["\']', html))


def validate_animated_shell(html: str) -> list[Finding]:
    findings: list[Finding] = []
    for attr in ('data-template="kai-report-creator"', "data-version=", "data-theme="):
        if attr.replace('"', "'") not in html and attr not in html:
            findings.append(Finding("animated.missing_attr", f"Missing marker: {attr}"))

    mode_match = re.search(r'data-animation=["\']([^"\']+)["\']', html)
    mode = mode_match.group(1) if mode_match else None
    if mode not in ANIMATED_MODES:
        findings.append(
            Finding("animated.invalid_mode", f"data-animation must be one of {ANIMATED_MODES}, got {mode!r}.")
        )

    # Frame chrome: keyboard paging + play mode
    if "keydown" not in html or "scrollIntoView" not in html:
        findings.append(Finding("animated.missing_paging", "Keyboard section paging (keydown + scrollIntoView) not found."))
    if "playing" not in html or "requestFullscreen" not in html:
        findings.append(Finding("animated.missing_play_mode", "Play mode (body.playing + requestFullscreen) not found."))
    if re.search(r"body\.playing\s*\{[^}]*overflow\s*:\s*hidden", html):
        findings.append(Finding("animated.playing_overflow_hidden", "body.playing must not set overflow:hidden (breaks paging)."))

    # Font policy: no external font origins
    for origin in FORBIDDEN_FONT_ORIGINS:
        if origin in html:
            findings.append(Finding("animated.external_font", f"External font origin forbidden: {origin}"))

    # External script policy
    ext_srcs = re.findall(r'<script\b[^>]*\bsrc=["\']([^"\']+)["\']', html)
    if mode == "iridescence":
        if ext_srcs:
            findings.append(Finding("animated.external_script", f"iridescence mode must have zero CDNs, found: {ext_srcs}"))
        if not re.search(r"getContext\(\s*['\"]webgl", html):
            findings.append(Finding("animated.missing_webgl", "iridescence mode requires a WebGL canvas."))
        elif "linear-gradient(135deg,#cfe0ff,#f0f6ff)" not in html:
            findings.append(Finding("animated.missing_webgl_fallback", "Missing WebGL-unavailable fallback gradient."))
    elif mode == "scrollytelling":
        for src in ext_srcs:
            if not src.startswith(ANIMATED_ALLOWED_SCRIPT_HOSTS):
                findings.append(Finding("animated.external_script", f"Script origin not allowed: {src}"))
        script_tags = re.findall(r"<script\b[^>]*\bsrc=[^>]*>", html)
        for tag in script_tags:
            if "integrity=" not in tag:
                findings.append(Finding("animated.missing_sri", f"CDN script missing integrity attr: {tag[:100]}"))
    return findings


THEME_MARKERS = {
    "corporate-blue": ["/* Theme: corporate-blue", "--font-sans:", "body { font-family: var(--font-sans)"],
    "minimal": ["/* Theme: minimal", "--font-sans:", "body { font-family: var(--font-sans)"],
    "dark-tech": ["/* Theme: dark-tech", "--font-mono:", "body { font-family: var(--font-sans)"],
    "dark-board": ["/* Theme: dark-board", "--font-mono:", "body { font-family: var(--font-sans)"],
    "data-story": ["/* Theme: data-story", "--font-sans:", "body { font-family: var(--font-sans)"],
    "newspaper": ["/* Theme: newspaper", "--font-sans:", "body { font-family: var(--font-sans)"],
    "regular-lumen": [
        "/* Theme: regular-lumen",
        "--bg: #F7F5F1",
        "--font-sans: 'Playfair Display'",
        "body { font-family: var(--font-sans)",
        ".report-wrapper { max-width: 920px",
        ".main-with-toc",
    ],
    "fangsong": [
        "/* Theme: fangsong",
        "--font-sans: 'FangSong'",
        "body { font-family: var(--font-sans-ui)",
        ".report-wrapper { max-width: 920px",
    ],
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return html_lib.unescape(text).strip()


def has_real_number(value: str) -> bool:
    return bool(re.search(r"\d", value)) and not PLACEHOLDER_RE.search(value)


def extract_theme(html: str) -> str | None:
    match = re.search(r'data-theme=["\']([^"\']+)["\']', html)
    return match.group(1) if match else None


def extract_summary_json(html: str) -> dict[str, object] | None:
    match = re.search(
        r'<script\b[^>]*id=["\']report-summary["\'][^>]*>\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def kpi_values_from_html(html: str) -> list[str]:
    pattern = re.compile(
        r'<div\b[^>]*class=["\'][^"\']*\bkpi-value\b[^"\']*["\'][^>]*>(.*?)</div>',
        re.DOTALL,
    )
    return [strip_tags(match.group(1)) for match in pattern.finditer(html)]


def validate_standard_shell(html: str) -> list[Finding]:
    findings: list[Finding] = []
    for element_id in STANDARD_REQUIRED_IDS:
        if f'id="{element_id}"' not in html and f"id='{element_id}'" not in html:
            findings.append(
                Finding("shell.missing_id", f"Missing standard shell element id={element_id!r}.")
            )
    if 'data-template="kai-report-creator"' not in html and "data-template='kai-report-creator'" not in html:
        findings.append(Finding("shell.missing_template_attr", "Missing data-template marker."))
    if 'data-version=' not in html:
        findings.append(Finding("shell.missing_version_attr", "Missing data-version marker."))
    if 'data-theme=' not in html:
        findings.append(Finding("shell.missing_theme_attr", "Missing data-theme marker."))
    return findings


def validate_theme_fidelity(html: str) -> list[Finding]:
    findings: list[Finding] = []
    theme = extract_theme(html)
    if not theme:
        return [Finding("theme.missing", "Missing data-theme attribute.")]

    markers = THEME_MARKERS.get(theme)
    if not markers:
        return findings

    for marker in markers:
        if marker not in html:
            findings.append(
                Finding("theme.fingerprint_mismatch", f"{theme} HTML missing theme marker: {marker}")
            )

    if theme == "regular-lumen":
        body_rule_match = re.search(r"body\s*\{[^}]*\}", html, re.DOTALL)
        body_rule = body_rule_match.group(0) if body_rule_match else ""
        if "max-width" in body_rule or re.search(r"padding\s*:\s*2rem", body_rule):
            findings.append(
                Finding(
                    "theme.regular_lumen_body_layout",
                    "regular-lumen must use .report-wrapper for width/padding, not body max-width/padding.",
                )
            )
        if "background-color: var(--bg)" in body_rule and "background: var(--bg)" not in body_rule:
            findings.append(
                Finding(
                    "theme.regular_lumen_background",
                    "regular-lumen body should preserve the theme background declaration.",
                )
            )
    return findings


def validate_kpi_values(html: str) -> list[Finding]:
    findings: list[Finding] = []
    for value in kpi_values_from_html(html):
        if not has_real_number(value):
            findings.append(Finding("kpi.invalid_value", f"Invalid KPI value: {value!r}."))

    summary = extract_summary_json(html)
    if not summary:
        findings.append(Finding("summary.invalid_json", "Missing or invalid report-summary JSON."))
        return findings

    kpis = summary.get("kpis", [])
    if not isinstance(kpis, list):
        findings.append(Finding("summary.invalid_kpis", "report-summary.kpis must be a list."))
        return findings

    for item in kpis:
        if not isinstance(item, dict):
            findings.append(Finding("summary.invalid_kpi_item", "Each summary KPI must be an object."))
            continue
        value = str(item.get("value", "")).strip()
        if value and not has_real_number(value):
            findings.append(Finding("summary.invalid_kpi_value", f"Invalid summary KPI value: {value!r}."))
    return findings


# ─── JSON-LD validation (v5.1) ───────────────────────────────────────────────

from html.parser import HTMLParser
from typing import List


class _JsonLdExtractor(HTMLParser):
    """Extract ld+json script contents from <head>, tracking position."""

    def __init__(self) -> None:
        super().__init__()
        self.in_head = False
        self.seen_title = False
        self.seen_style_or_link_css = False
        self.scripts: list[tuple[str, bool]] = []
        self._in_ld_script = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "head":
            self.in_head = True
            return
        if not self.in_head:
            return
        if tag == "title":
            self.seen_title = True
        elif tag == "style":
            self.seen_style_or_link_css = True
        elif tag == "link":
            attrs_d = dict(attrs)
            rel = (attrs_d.get("rel") or "").lower()
            if "stylesheet" in rel.split():
                self.seen_style_or_link_css = True
        elif tag == "script":
            attrs_d = dict(attrs)
            type_attr = (attrs_d.get("type") or "").strip().lower()
            if type_attr == "application/ld+json":
                self._in_ld_script = True
                self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self.in_head = False
        elif tag == "script" and self._in_ld_script:
            content = "".join(self._buffer)
            valid_position = self.seen_title and not self.seen_style_or_link_css
            self.scripts.append((content, valid_position))
            self._in_ld_script = False
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._in_ld_script:
            self._buffer.append(data)


_LDJSON_BLOCK_RE = re.compile(
    r'<script\b[^>]*\btype\s*=\s*["\']?application/ld\+json\s*["\']?[^>]*>(.*?)</script\s*>',
    re.DOTALL | re.IGNORECASE,
)
_LDJSON_SCRIPT_OPEN_RE = re.compile(
    r'<script\b[^>]*\btype\s*=\s*["\']?application/ld\+json\s*["\']?[^>]*>',
    re.IGNORECASE,
)
_HASH_STRICT_RE = re.compile(r"sha256:[a-f0-9]{16}")

_ALLOWED_PROPERTY_IDS = frozenset({
    "https://kai.app/ns#reportTheme",
    "https://kai.app/ns#reportTemplate",
    "https://kai.app/ns#rendererVersion",
    "https://kai.app/ns#irHash",
    "https://kai.app/ns#metadataVersion",
})


def check_jsonld(html: str) -> list[Finding]:
    """Validate schema.org JSON-LD embedded in <head>. Returns empty list on success."""
    findings: list[Finding] = []

    # <head> must exist
    head_match = re.search(r"<head\b[^>]*>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    if not head_match:
        if _LDJSON_SCRIPT_OPEN_RE.search(html):
            findings.append(Finding("jsonld.position_invalid", "<head> not found; JSON-LD must be inside <head>"))
        else:
            findings.append(Finding("jsonld.missing", "no <head> and no ld+json script found"))
        return findings

    head_html = head_match.group(1)

    # Raw source-level checks (before HTMLParser which may truncate on raw </script>)
    raw_blocks = _LDJSON_BLOCK_RE.findall(head_html)
    open_tags = _LDJSON_SCRIPT_OPEN_RE.findall(head_html)

    # Multiple blocks
    if len(open_tags) > 1:
        findings.append(Finding("jsonld.multiple", f"only one ld+json script allowed in <head>, found {len(open_tags)}"))
        return findings

    # Open tag but no complete block → likely raw </script> truncation
    if not raw_blocks:
        if open_tags:
            findings.append(Finding(
                "jsonld.escaping_unsafe",
                "ld+json open tag found but cannot extract complete block; likely raw </script> in JSON; use <\\/script>",
            ))
        elif _LDJSON_SCRIPT_OPEN_RE.search(html):
            findings.append(Finding("jsonld.position_invalid", "ld+json script must be in <head>, not <body>"))
        else:
            findings.append(Finding("jsonld.missing", "no <script type='application/ld+json'> in <head>"))
        return findings

    # Raw escaping check
    raw_content = raw_blocks[0]
    if re.search(r"</script", raw_content, re.IGNORECASE):
        findings.append(Finding("jsonld.escaping_unsafe", "raw </script substring; must be <\\/script"))
        return findings
    if "\u2028" in raw_content or "\u2029" in raw_content:
        findings.append(Finding("jsonld.escaping_unsafe", "raw U+2028/U+2029 must be \\u2028/\\u2029"))
        return findings

    # HTMLParser extraction + position
    parser = _JsonLdExtractor()
    parser.feed(html)
    if not parser.scripts:
        findings.append(Finding("jsonld.parse_error", "extractor failed; check HTML structure"))
        return findings
    if len(parser.scripts) > 1:
        findings.append(Finding("jsonld.multiple", f"only one ld+json script allowed, found {len(parser.scripts)}"))
        return findings

    content, valid_position = parser.scripts[0]
    if not valid_position:
        findings.append(Finding(
            "jsonld.position_invalid",
            "JSON-LD must be after <title> and before first <style> or <link rel=stylesheet>",
        ))

    # JSON parse
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        findings.append(Finding("jsonld.parse_error", f"json parse failed: {e}"))
        return findings

    # Required fields
    if data.get("@context") != "http://schema.org/":
        findings.append(Finding("jsonld.field_missing", f"@context must be 'http://schema.org/', got {data.get('@context')!r}"))
    if data.get("@type") != "Report":
        findings.append(Finding("jsonld.field_missing", f"@type must be 'Report', got {data.get('@type')!r}"))
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        findings.append(Finding("jsonld.field_missing", "name must be non-empty string"))
    if data.get("inLanguage") not in ("zh-CN", "en-US"):
        findings.append(Finding("jsonld.field_missing", f"inLanguage must be 'zh-CN' or 'en-US', got {data.get('inLanguage')!r}"))

    creator = data.get("creator")
    if not isinstance(creator, dict):
        findings.append(Finding("jsonld.field_missing", "creator must be object"))
    else:
        if creator.get("@type") not in ("Person", "Organization"):
            findings.append(Finding("jsonld.field_missing", f"creator.@type must be Person|Organization, got {creator.get('@type')!r}"))
        if not isinstance(creator.get("name"), str) or not creator["name"].strip():
            findings.append(Finding("jsonld.field_missing", "creator.name must be non-empty string"))

    # additionalProperty
    aps = data.get("additionalProperty", [])
    if not isinstance(aps, list):
        findings.append(Finding("jsonld.field_missing", "additionalProperty must be array"))
        aps = []

    metadata_version_pv = next(
        (ap for ap in aps if isinstance(ap, dict) and ap.get("propertyID") == "https://kai.app/ns#metadataVersion"),
        None,
    )
    if not metadata_version_pv:
        findings.append(Finding("jsonld.field_missing", "additionalProperty missing metadataVersion"))
    elif metadata_version_pv.get("value") != "1":
        findings.append(Finding("jsonld.field_missing", f"metadataVersion value must be '1', got {metadata_version_pv.get('value')!r}"))

    # meta ir-hash parity (v5.1: case-sensitive hash validation)
    meta_open_match = re.search(r'<meta\b[^>]*\bname\s*=\s*["\']ir-hash["\'][^>]*>', html, re.IGNORECASE)
    meta_content_match = re.search(
        r'<meta\b(?=[^>]*\bname\s*=\s*["\']ir-hash["\'])[^>]*\bcontent\s*=\s*["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    )
    meta_strict_value: str | None = None
    if meta_content_match:
        content_str = meta_content_match.group(1)
        if _HASH_STRICT_RE.fullmatch(content_str):
            meta_strict_value = content_str
        else:
            findings.append(Finding(
                "jsonld.hash_invalid",
                f"meta ir-hash content does not match 'sha256:[a-f0-9]{{16}}' (lowercase), got {content_str!r}",
            ))

    at_id = data.get("@id")
    ir_hash_pv = next(
        (ap for ap in aps if isinstance(ap, dict) and ap.get("propertyID") == "https://kai.app/ns#irHash"),
        None,
    )

    if meta_strict_value:
        meta_hex = meta_strict_value.split(":", 1)[1]
        expected_id = f"https://kai.app/id/report/{meta_hex}"
        if not at_id:
            findings.append(Finding("jsonld.field_missing", f"meta ir-hash present but JSON-LD @id missing; expected {expected_id!r}"))
        elif at_id != expected_id:
            findings.append(Finding("jsonld.field_missing", f"@id must be {expected_id!r}, got {at_id!r}"))
        if not ir_hash_pv:
            findings.append(Finding("jsonld.field_missing", f"meta ir-hash present but irHash PropertyValue missing; expected value {meta_hex!r}"))
        elif ir_hash_pv.get("value") != meta_hex:
            findings.append(Finding("jsonld.field_missing", f"irHash value must be {meta_hex!r}, got {ir_hash_pv.get('value')!r}"))
    elif not meta_open_match:
        # No meta → @id and irHash should not be present
        if at_id is not None:
            findings.append(Finding("jsonld.field_unexpected", f"meta ir-hash absent but @id={at_id!r} present; remove @id when no meta"))
        if ir_hash_pv is not None:
            findings.append(Finding("jsonld.field_unexpected", "meta ir-hash absent but irHash PropertyValue present; remove when no meta"))

    # additionalType prefix
    add_type = data.get("additionalType")
    if add_type is not None and not (isinstance(add_type, str) and add_type.startswith("https://kai.app/ns#report-archetype-")):
        findings.append(Finding("jsonld.field_missing", f"additionalType must start with kai.app/ns#report-archetype- prefix, got {add_type!r}"))

    # propertyID allow-list
    for ap in aps:
        if isinstance(ap, dict):
            pid = ap.get("propertyID", "")
            if pid and pid not in _ALLOWED_PROPERTY_IDS:
                findings.append(Finding("jsonld.iri_unwhitelisted", f"unallowed propertyID: {pid!r}"))

    # @id prefix check
    if at_id is not None and not (isinstance(at_id, str) and at_id.startswith("https://kai.app/id/report/")):
        findings.append(Finding("jsonld.field_missing", f"@id must start with 'https://kai.app/id/report/', got {at_id!r}"))

    # lang consistency
    html_lang_match = re.search(r'<html\b[^>]*\blang\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    if html_lang_match:
        h_lang = html_lang_match.group(1).lower()
        i_lang = (data.get("inLanguage") or "").lower()
        if h_lang and i_lang and h_lang != i_lang:
            if not (h_lang.startswith(i_lang.split("-")[0]) or i_lang.startswith(h_lang.split("-")[0])):
                findings.append(Finding("jsonld.lang_mismatch", f"<html lang>={h_lang!r} vs inLanguage={i_lang!r}"))

    # theme consistency
    html_theme_match = re.search(r'data-theme\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    if html_theme_match:
        h_theme = html_theme_match.group(1)
        report_theme_pv = next(
            (ap for ap in aps if isinstance(ap, dict) and ap.get("propertyID") == "https://kai.app/ns#reportTheme"),
            None,
        )
        if not report_theme_pv:
            findings.append(Finding("jsonld.field_missing", f"data-theme={h_theme!r} present but reportTheme PropertyValue missing"))
        elif report_theme_pv.get("value") != h_theme:
            findings.append(Finding("jsonld.theme_mismatch", f"data-theme={h_theme!r} vs reportTheme={report_theme_pv.get('value')!r}"))

    return findings


def validate_html_text(
    html: str,
    *,
    standard_shell: bool = True,
    theme_fidelity: bool = True,
    kpi_values: bool = True,
    jsonld_check: bool = True,
) -> dict[str, object]:
    findings: list[Finding] = []
    animated = is_animated_html(html)
    if animated:
        findings.extend(validate_animated_shell(html))
    if standard_shell and not animated:
        findings.extend(validate_standard_shell(html))
    if theme_fidelity and not animated:
        findings.extend(validate_theme_fidelity(html))
    if kpi_values:
        findings.extend(validate_kpi_values(html))
    if jsonld_check:
        findings.extend(check_jsonld(html))

    return {
        "status": "valid" if not findings else "invalid",
        "findings": [asdict(finding) for finding in findings],
        "exit_code": 0 if not findings else 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate final HTML report quality gates.")
    parser.add_argument("html_path", help="Path to generated HTML report")
    parser.add_argument("--no-standard-shell", action="store_true", help="Skip standard shell checks")
    parser.add_argument("--no-theme-fidelity", action="store_true", help="Skip theme fidelity checks")
    parser.add_argument("--no-kpi-values", action="store_true", help="Skip KPI value checks")
    parser.add_argument("--no-jsonld-check", action="store_true", help="Skip JSON-LD metadata checks")
    args = parser.parse_args()

    html_text = Path(args.html_path).read_text(encoding="utf-8")
    report = validate_html_text(
        html_text,
        standard_shell=not args.no_standard_shell,
        theme_fidelity=not args.no_theme_fidelity,
        kpi_values=not args.no_kpi_values,
        jsonld_check=not args.no_jsonld_check,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(int(report["exit_code"]))


if __name__ == "__main__":
    main()
