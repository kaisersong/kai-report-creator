"""JSON-LD quality gate tests — covers v5.1 design §5 test matrix #1-#31."""
from __future__ import annotations

import json
import pytest
from scripts.html_quality_gate import check_jsonld, validate_html_text, Finding


def _wrap(head_content: str = "", body_content: str = "", lang: str = "zh-CN", theme: str = "corporate-blue", meta_hash: str | None = None) -> str:
    """Build minimal HTML shell for testing."""
    meta_ir = f'\n    <meta name="ir-hash" content="sha256:{meta_hash}">' if meta_hash else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-template="kai-report-creator" data-version="1.23.0" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <title>Test Report</title>{meta_ir}
{head_content}
    <style>:root {{ --primary: #000; }}</style>
</head>
<body>
{body_content}
</body>
</html>"""


def _valid_jsonld(
    name: str = "Test Report",
    context: str = "http://schema.org/",
    type_: str = "Report",
    in_language: str = "zh-CN",
    creator_type: str = "Organization",
    creator_name: str = "kai-report-creator",
    theme: str = "corporate-blue",
    at_id: str | None = None,
    ir_hash: str | None = None,
    archetype: str | None = None,
    extra_props: list | None = None,
) -> str:
    """Build a valid JSON-LD payload string."""
    payload: dict = {
        "@context": context,
        "@type": type_,
        "name": name,
        "inLanguage": in_language,
        "creator": {"@type": creator_type, "name": creator_name},
        "additionalProperty": [
            {"@type": "PropertyValue", "propertyID": "https://kai.app/ns#reportTheme", "value": theme},
            {"@type": "PropertyValue", "propertyID": "https://kai.app/ns#metadataVersion", "value": "1"},
        ],
    }
    if at_id:
        payload["@id"] = at_id
    if ir_hash:
        payload["additionalProperty"].append(
            {"@type": "PropertyValue", "propertyID": "https://kai.app/ns#irHash", "value": ir_hash}
        )
    if archetype:
        payload["additionalType"] = f"https://kai.app/ns#report-archetype-{archetype}"
    if extra_props:
        payload["additionalProperty"].extend(extra_props)
    return json.dumps(payload, ensure_ascii=False)


def _jsonld_script(payload_str: str) -> str:
    escaped = payload_str.replace("</", "<\\/")
    return f'    <script type="application/ld+json">{escaped}</script>'


VALID_HASH = "abc123def4567890"


class TestCheckJsonldPresence:
    """#1-#4: presence and position checks."""

    def test_missing_jsonld(self):
        """#1: no JSON-LD → jsonld.missing"""
        html = _wrap()
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.missing" for f in findings)

    def test_jsonld_in_body(self):
        """#2: JSON-LD in <body> → jsonld.position_invalid"""
        script = _jsonld_script(_valid_jsonld())
        html = _wrap(body_content=script)
        findings = check_jsonld(html)
        codes = [f.code for f in findings]
        assert "jsonld.position_invalid" in codes or "jsonld.missing" in codes

    def test_jsonld_after_style(self):
        """#3: JSON-LD after <style> → jsonld.position_invalid"""
        payload = _valid_jsonld()
        escaped_payload = payload.replace("</", "<\\/")
        html = (
            '<!DOCTYPE html>\n'
            '<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">\n'
            '<head>\n'
            '    <title>Test</title>\n'
            '    <style>:root { --x: 1; }</style>\n'
            f'    <script type="application/ld+json">{escaped_payload}</script>\n'
            '</head>\n'
            '<body></body>\n'
            '</html>'
        )
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.position_invalid" for f in findings)

    def test_jsonld_after_link_stylesheet(self):
        """#4: JSON-LD after <link rel=stylesheet> → jsonld.position_invalid"""
        payload = _valid_jsonld()
        escaped_payload = payload.replace("</", "<\\/")
        html = (
            '<!DOCTYPE html>\n'
            '<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">\n'
            '<head>\n'
            '    <title>Test</title>\n'
            '    <link rel="stylesheet" href="x.css">\n'
            f'    <script type="application/ld+json">{escaped_payload}</script>\n'
            '    <style>:root { --x: 1; }</style>\n'
            '</head>\n'
            '<body></body>\n'
            '</html>'
        )
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.position_invalid" for f in findings)


class TestCheckJsonldEscaping:
    """#5-#7: escaping checks."""

    def test_raw_script_close(self):
        """#5: raw </script> in string → escaping_unsafe or parse_error"""
        bad_payload = '{"@context":"http://schema.org/","@type":"Report","name":"evil </script><img>"}'
        html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">
<head>
    <title>Test</title>
    <script type="application/ld+json">{bad_payload}</script>
    <style>:root {{ --x: 1; }}</style>
</head>
<body></body>
</html>"""
        findings = check_jsonld(html)
        codes = [f.code for f in findings]
        assert "jsonld.escaping_unsafe" in codes or "jsonld.parse_error" in codes

    def test_raw_script_close_case_insensitive(self):
        """#6: raw </Script> → escaping_unsafe or parse_error"""
        bad_payload = '{"@context":"http://schema.org/","@type":"Report","name":"evil </Script>"}'
        html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">
<head>
    <title>Test</title>
    <script type="application/ld+json">{bad_payload}</script>
    <style>:root {{ --x: 1; }}</style>
</head>
<body></body>
</html>"""
        findings = check_jsonld(html)
        codes = [f.code for f in findings]
        assert "jsonld.escaping_unsafe" in codes or "jsonld.parse_error" in codes

    def test_raw_u2028(self):
        """#7: raw U+2028 → jsonld.escaping_unsafe"""
        payload = _valid_jsonld()
        # Insert U+2028 in the payload
        payload_with_u2028 = payload[:20] + "\u2028" + payload[20:]
        script = f'    <script type="application/ld+json">{payload_with_u2028}</script>'
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.escaping_unsafe" for f in findings)


class TestCheckJsonldFields:
    """#8-#14: required field checks."""

    def test_wrong_context(self):
        """#8"""
        script = _jsonld_script(_valid_jsonld(context="https://schema.org/"))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "@context" in f.message for f in findings)

    def test_wrong_type(self):
        """#9"""
        script = _jsonld_script(_valid_jsonld(type_="WebPage"))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "@type" in f.message for f in findings)

    def test_missing_metadata_version(self):
        """#10"""
        payload = json.loads(_valid_jsonld())
        payload["additionalProperty"] = [ap for ap in payload["additionalProperty"] if ap.get("propertyID") != "https://kai.app/ns#metadataVersion"]
        script = _jsonld_script(json.dumps(payload))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "metadataVersion" in f.message for f in findings)

    def test_wrong_metadata_version_value(self):
        """#11"""
        payload = json.loads(_valid_jsonld())
        for ap in payload["additionalProperty"]:
            if ap.get("propertyID") == "https://kai.app/ns#metadataVersion":
                ap["value"] = "2"
        script = _jsonld_script(json.dumps(payload))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "metadataVersion" in f.message for f in findings)

    def test_wrong_creator_type(self):
        """#12"""
        script = _jsonld_script(_valid_jsonld(creator_type="Thing"))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "creator" in f.message for f in findings)

    def test_empty_creator_name(self):
        """#13"""
        script = _jsonld_script(_valid_jsonld(creator_name=""))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "creator.name" in f.message for f in findings)

    def test_wrong_inlanguage(self):
        """#14"""
        script = _jsonld_script(_valid_jsonld(in_language="zh"))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "inLanguage" in f.message for f in findings)


class TestCheckJsonldIRI:
    """#15-#19: IRI and prefix checks."""

    def test_unallowed_property_id(self):
        """#15"""
        script = _jsonld_script(_valid_jsonld(extra_props=[{"@type": "PropertyValue", "propertyID": "http://evil.com/x", "value": "bad"}]))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.iri_unwhitelisted" for f in findings)

    def test_bad_id_prefix(self):
        """#16"""
        script = _jsonld_script(_valid_jsonld(at_id="javascript:alert(1)"))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "@id" in f.message for f in findings)

    def test_id_meta_mismatch(self):
        """#17"""
        script = _jsonld_script(_valid_jsonld(at_id=f"https://kai.app/id/report/wronghash1234567", ir_hash="wronghash1234567"))
        html = _wrap(head_content=script, meta_hash=VALID_HASH)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "@id" in f.message for f in findings)

    def test_irhash_has_prefix(self):
        """#18: irHash value contains 'sha256:' prefix → fail"""
        script = _jsonld_script(_valid_jsonld(at_id=f"https://kai.app/id/report/{VALID_HASH}", ir_hash=f"sha256:{VALID_HASH}"))
        html = _wrap(head_content=script, meta_hash=VALID_HASH)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "irHash" in f.message for f in findings)

    def test_bad_additional_type_prefix(self):
        """#19"""
        payload = json.loads(_valid_jsonld())
        payload["additionalType"] = "research"  # bare string, no prefix
        script = _jsonld_script(json.dumps(payload))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "additionalType" in f.message for f in findings)


class TestCheckJsonldConsistency:
    """#20-#22: lang/theme consistency."""

    def test_lang_mismatch(self):
        """#20"""
        script = _jsonld_script(_valid_jsonld(in_language="en-US"))
        html = _wrap(head_content=script, lang="zh-CN")
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.lang_mismatch" for f in findings)

    def test_theme_missing_reporttheme(self):
        """#21"""
        payload = json.loads(_valid_jsonld())
        payload["additionalProperty"] = [ap for ap in payload["additionalProperty"] if ap.get("propertyID") != "https://kai.app/ns#reportTheme"]
        script = _jsonld_script(json.dumps(payload))
        html = _wrap(head_content=script)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "reportTheme" in f.message for f in findings)

    def test_theme_mismatch(self):
        """#22"""
        script = _jsonld_script(_valid_jsonld(theme="minimal"))
        html = _wrap(head_content=script, theme="corporate-blue")
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.theme_mismatch" for f in findings)


class TestCheckJsonldMetaParity:
    """#23-#24, #29-#31: meta hash parity checks."""

    def test_meta_present_but_id_missing(self):
        """#23"""
        script = _jsonld_script(_valid_jsonld())  # no @id
        html = _wrap(head_content=script, meta_hash=VALID_HASH)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "@id missing" in f.message for f in findings)

    def test_meta_present_but_irhash_pv_missing(self):
        """#24"""
        script = _jsonld_script(_valid_jsonld(at_id=f"https://kai.app/id/report/{VALID_HASH}"))  # no irHash PV
        html = _wrap(head_content=script, meta_hash=VALID_HASH)
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_missing" and "irHash PropertyValue" in f.message for f in findings)

    def test_uppercase_meta_hash(self):
        """#29: uppercase hex → jsonld.hash_invalid"""
        script = _jsonld_script(_valid_jsonld())
        html = _wrap(head_content=script).replace('content="sha256:', 'content="sha256:').replace("</head>", "</head>")
        # Manually build with uppercase
        html_upper = f"""<!DOCTYPE html>
<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">
<head>
    <title>Test Report</title>
    <meta name="ir-hash" content="sha256:ABCDEF1234567890">
{_jsonld_script(_valid_jsonld())}
    <style>:root {{ --x: 1; }}</style>
</head>
<body></body>
</html>"""
        findings = check_jsonld(html_upper)
        assert any(f.code == "jsonld.hash_invalid" for f in findings)

    def test_meta_wrong_length(self):
        """#30: hex length ≠ 16 → jsonld.hash_invalid"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">
<head>
    <title>Test Report</title>
    <meta name="ir-hash" content="sha256:abc123">
{_jsonld_script(_valid_jsonld())}
    <style>:root {{ --x: 1; }}</style>
</head>
<body></body>
</html>"""
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.hash_invalid" for f in findings)

    def test_meta_absent_but_id_present(self):
        """#31: meta absent but @id present → jsonld.field_unexpected"""
        script = _jsonld_script(_valid_jsonld(at_id="https://kai.app/id/report/abc123def4567890"))
        html = _wrap(head_content=script)  # no meta_hash
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.field_unexpected" for f in findings)


class TestCheckJsonldMultipleBlocks:
    """#28: multiple ld+json blocks → jsonld.multiple"""

    def test_two_blocks(self):
        script1 = _jsonld_script(_valid_jsonld())
        script2 = _jsonld_script(_valid_jsonld(name="Second"))
        html = _wrap(head_content=f"{script1}\n{script2}")
        findings = check_jsonld(html)
        assert any(f.code == "jsonld.multiple" for f in findings)


class TestCheckJsonldVariants:
    """#25-#26: type attribute variants."""

    def test_trailing_space_type(self):
        """#25: type="application/ld+json " (trailing space) should still be extracted"""
        payload = _valid_jsonld()
        escaped_payload = payload.replace("</", "<\\/")
        html = (
            '<!DOCTYPE html>\n'
            '<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">\n'
            '<head>\n'
            '    <title>Test Report</title>\n'
            f'    <script type="application/ld+json ">{escaped_payload}</script>\n'
            '    <style>:root { --x: 1; }</style>\n'
            '</head>\n'
            '<body></body>\n'
            '</html>'
        )
        findings = check_jsonld(html)
        # Should NOT be missing (extractor uses strip+lowercase)
        assert not any(f.code == "jsonld.missing" for f in findings)

    def test_single_quote_type(self):
        """#26: type='application/ld+json' with single quotes"""
        payload = _valid_jsonld()
        escaped_payload = payload.replace("</", "<\\/")
        html = (
            '<!DOCTYPE html>\n'
            '<html lang="zh-CN" data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">\n'
            '<head>\n'
            '    <title>Test Report</title>\n'
            f"    <script type='application/ld+json'>{escaped_payload}</script>\n"
            '    <style>:root { --x: 1; }</style>\n'
            '</head>\n'
            '<body></body>\n'
            '</html>'
        )
        findings = check_jsonld(html)
        assert not any(f.code == "jsonld.missing" for f in findings)


class TestCheckJsonldValid:
    """#27: complete valid payload → empty findings."""

    def test_valid_full_payload(self):
        script = _jsonld_script(_valid_jsonld(
            at_id=f"https://kai.app/id/report/{VALID_HASH}",
            ir_hash=VALID_HASH,
        ))
        html = _wrap(head_content=script, meta_hash=VALID_HASH)
        findings = check_jsonld(html)
        assert findings == [], f"Expected no findings, got: {[f.code for f in findings]}"


class TestValidateHtmlTextJsonldFlag:
    """#32-#34: validate_html_text jsonld_check flag."""

    def test_returns_dict(self):
        """#32"""
        html = _wrap()
        result = validate_html_text(html, standard_shell=False, theme_fidelity=False, kpi_values=False, jsonld_check=False)
        assert "status" in result and "findings" in result and "exit_code" in result

    def test_jsonld_check_false_skips(self):
        """#33"""
        html = _wrap()  # no JSON-LD
        result = validate_html_text(html, standard_shell=False, theme_fidelity=False, kpi_values=False, jsonld_check=False)
        assert result["status"] == "valid"

    def test_jsonld_check_default_true(self):
        """#34"""
        html = _wrap()  # no JSON-LD
        result = validate_html_text(html, standard_shell=False, theme_fidelity=False, kpi_values=False)
        assert result["status"] == "invalid"
        assert any("jsonld" in f["code"] for f in result["findings"])
