from pathlib import Path

from scripts.html_quality_gate import validate_html_text


ROOT = Path(__file__).resolve().parent.parent


def test_html_quality_gate_rejects_handrolled_regular_lumen_shell():
    html = """
<!DOCTYPE html>
<html lang="zh" data-template="kai-report-creator" data-version="1.23.0" data-theme="regular-lumen">
<head>
<style>
/* regular-lumen theme CSS */
body {
  font-family: system-ui, -apple-system, sans-serif;
  background-color: var(--bg);
  padding: 2rem;
  max-width: 1200px;
}
</style>
</head>
<body>
<script type="application/json" id="report-summary">{"title":"T","sections":[],"kpis":[]}</script>
<h1>报告</h1>
</body>
</html>
""".strip()
    report = validate_html_text(html)
    codes = {finding["code"] for finding in report["findings"]}
    messages = "\n".join(finding["message"] for finding in report["findings"])

    assert report["status"] == "invalid"
    assert "shell.missing_id" in codes
    assert "theme.fingerprint_mismatch" in codes
    assert "theme.regular_lumen_body_layout" in codes
    assert "body max-width/padding" in messages
    assert "Playfair Display" in messages
    assert ".report-wrapper" in messages


def test_html_quality_gate_rejects_placeholder_and_status_kpi_values():
    html = """
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">
<head><style>/* Theme: corporate-blue */ --font-sans: x; body { font-family: var(--font-sans) }</style></head>
<body>
<script type="application/json" id="report-summary">
{"title":"T","sections":[],"kpis":[{"label":"会议数","value":"[数据待填写]"}]}
</script>
<button id="toc-toggle-btn"></button><nav id="toc-sidebar"></nav>
<button id="card-mode-btn"></button><div id="sc-overlay"></div>
<div id="edit-hotzone"></div><button id="edit-toggle"></button>
<button id="export-btn"></button><div id="export-menu"></div>
<button id="export-print"></button><button id="export-png-desktop"></button>
<button id="export-png-mobile"></button><button id="export-im-share"></button>
<div class="kpi-value">通过</div>
</body>
</html>
""".strip()
    report = validate_html_text(html, theme_fidelity=False)
    codes = [finding["code"] for finding in report["findings"]]

    assert report["status"] == "invalid"
    assert "kpi.invalid_value" in codes
    assert "summary.invalid_kpi_value" in codes


def test_html_quality_gate_accepts_regular_lumen_theme_fidelity_without_shell_check():
    html = (ROOT / "templates" / "zh" / "regular-lumen.html").read_text(encoding="utf-8")
    report = validate_html_text(html, standard_shell=False, jsonld_check=False)

    assert report["status"] == "valid"


def test_html_quality_gate_accepts_fangsong_theme_fidelity_without_shell_check():
    theme_css = (ROOT / "templates" / "themes" / "fangsong.css").read_text(encoding="utf-8")
    html = f"""
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.23.0" data-theme="fangsong">
<head><style>{theme_css}</style></head>
<body>
<script type="application/json" id="report-summary">{{"title":"T","sections":[],"kpis":[]}}</script>
</body>
</html>
""".strip()

    report = validate_html_text(html, standard_shell=False, jsonld_check=False)

    assert report["status"] == "valid"



# ─── animated render mode ────────────────────────────────────────────────────
# Regression guards for the bypasses found in the adversarial review; see
# proposals/animated-mode-fixes.md. The gate must reject anything that only
# *looks* like animated chrome (comments, JS strings, inert elements).

GSAP = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"
GSAP_SRI = ("sha512-7eHRwcbYkK4d9g/6tD/mhkf++eoTHwpNM9woBxtPUBWm67zeAfFC+HrdoE2Gan"
            "Keocly/VxeLvIqwvCdk7qScg==")
ST = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"
ST_SRI = ("sha512-onMTRKJBKz8M1TnqqDuGBlowlH0ohFzMXYRNebz+yOcc5TQr/zAKsthzhuv0hiy"
          "UKEiQEQXEynnXCvNTOk50dg==")
CU = "https://cdnjs.cloudflare.com/ajax/libs/countup.js/2.8.0/countUp.umd.min.js"
CU_SRI = ("sha512-kUIpdMjMlkYUVQgR3wVXJtmuwoD+G69Zt9JBa2rPH4C/+VPlAsQWKcqCv0SpJ8An"
          "ezBjfuM2JDjnc58Ee8Filw==")

JSONLD = """<script type="application/ld+json">
{"@context":"http://schema.org/","@type":"Report","name":"T","inLanguage":"zh-CN",
"creator":{"@type":"Organization","name":"kai-report-creator"},
"additionalProperty":[
{"@type":"PropertyValue","propertyID":"https://kai.app/ns#reportTheme","value":"__MODE__"},
{"@type":"PropertyValue","propertyID":"https://kai.app/ns#metadataVersion","value":"1"}]}
</script>"""


def _animated_html(mode="iridescence", *, chrome=None, scripts="", body="",
                   kpis='[{"label":"营收","value":"282.4亿"}]', theme=None):
    """A minimal but *honest* animated document: real chrome elements, real data."""
    if chrome is None:
        chrome = ('<button id="play-btn">▶</button>'
                  '<nav id="nav-sections"><a href="#s1">S1</a></nav>')
    if not scripts and mode == "scrollytelling":
        scripts = (f'<script src="{GSAP}" integrity="{GSAP_SRI}" crossorigin="anonymous"></script>'
                   f'<script src="{ST}" integrity="{ST_SRI}" crossorigin="anonymous"></script>'
                   f'<script src="{CU}" integrity="{CU_SRI}" crossorigin="anonymous"></script>')
    webgl = ("const gl=canvas.getContext('webgl');"
             "if(!gl){canvas.style.background='linear-gradient(135deg,#cfe0ff,#f0f6ff)';}"
             if mode == "iridescence" else "")
    return f"""<!DOCTYPE html>
<html lang="zh" data-template="kai-report-creator" data-version="1.24.0"
 data-theme="{theme or mode}" data-render-mode="animated" data-animation="{mode}">
<head><title>T</title>{JSONLD.replace("__MODE__", theme or mode)}{scripts}</head>
<body>
<script type="application/json" id="report-summary">{{"title":"T","sections":["s1"],"kpis":{kpis}}}</script>
{chrome}
<section id="s1">S1</section>
{body}
<script>
{webgl}
const secs=[...document.querySelectorAll('section')];
document.addEventListener('keydown',e=>{{ if(e.key==='ArrowDown') secs[0].scrollIntoView({{behavior:'smooth'}}); }});
document.getElementById('play-btn').addEventListener('click',()=>{{
  document.body.classList.toggle('playing'); document.documentElement.requestFullscreen();
}});
</script>
</body></html>"""


def _codes(html, **kw):
    return {f["code"] for f in validate_html_text(html, **kw)["findings"]}


def test_animated_iridescence_valid_on_full_default_path():
    """Honest document passes with every check on, JSON-LD included."""
    report = validate_html_text(_animated_html("iridescence"))
    assert report["status"] == "valid", report["findings"]


def test_animated_scrollytelling_valid_with_pinned_scripts():
    report = validate_html_text(_animated_html("scrollytelling"))
    assert report["status"] == "valid", report["findings"]


def test_animated_skips_standard_shell_ids():
    assert "shell.missing_id" not in _codes(_animated_html("iridescence"))


def test_animated_rejects_missing_chrome():
    codes = _codes(_animated_html("iridescence", chrome=""), jsonld_check=False)
    assert "animated.missing_chrome" in codes


def test_animated_rejects_chrome_ids_forged_in_comment():
    forged = '<!-- <button id="play-btn"></button><nav id="nav-sections"></nav> -->'
    codes = _codes(_animated_html("iridescence", chrome=forged), jsonld_check=False)
    assert "animated.missing_chrome" in codes


def test_animated_rejects_chrome_ids_forged_in_script_string():
    forged = """<script>const x='<button id="play-btn"><nav id="nav-sections">';</script>"""
    codes = _codes(_animated_html("iridescence", chrome=forged), jsonld_check=False)
    assert "animated.missing_chrome" in codes


def test_animated_rejects_chrome_ids_hidden_in_inert_elements():
    """`</style>` used to reset the skip counter and expose template content."""
    forged = ('<template></style><button id="play-btn"></button>'
              '<nav id="nav-sections"></nav></template>')
    codes = _codes(_animated_html("iridescence", chrome=forged), jsonld_check=False)
    assert "animated.missing_chrome" in codes


def test_render_mode_not_hijacked_by_comment():
    from scripts.html_quality_gate import is_animated_html
    standard = '<!DOCTYPE html><html data-theme="minimal"><body>' \
               '<!-- data-render-mode="animated" --></body></html>'
    assert is_animated_html(standard) is False


def test_render_mode_not_hijacked_by_rcdata_fake_root():
    from scripts.html_quality_gate import is_animated_html
    hijack = ('<title><html data-render-mode="animated"></title>'
              '<html data-render-mode="standard"><body>x</body></html>')
    assert is_animated_html(hijack) is False


def test_animated_requires_theme_to_match_mode():
    codes = _codes(_animated_html("iridescence", theme="bogus-theme"), jsonld_check=False)
    assert "animated.theme_mode_mismatch" in codes


def test_animated_iridescence_rejects_any_external_script():
    unquoted = "<script src=https://evil.example/payload.js></script>"
    codes = _codes(_animated_html("iridescence", body=unquoted), jsonld_check=False)
    assert "animated.external_script" in codes


def test_animated_scrollytelling_rejects_forged_integrity():
    scripts = f'<script src="{GSAP}" integrity="sha512-{"A" * 40}"></script>'
    codes = _codes(_animated_html("scrollytelling", scripts=scripts), jsonld_check=False)
    assert "animated.external_script" in codes
    assert "animated.missing_pinned_script" in codes


def test_animated_scrollytelling_rejects_lookalike_path():
    evil = GSAP.replace("libs/gsap/3.12.5", "libs/evil/1")
    scripts = (f'<script src="{evil}" integrity="{GSAP_SRI}"></script>'
               f'<script src="{ST}" integrity="{ST_SRI}"></script>'
               f'<script src="{CU}" integrity="{CU_SRI}"></script>')
    codes = _codes(_animated_html("scrollytelling", scripts=scripts), jsonld_check=False)
    assert "animated.external_script" in codes
    assert "animated.missing_pinned_script" in codes


def test_animated_rejects_empty_and_missing_summary_kpis():
    empty_value = _codes(_animated_html("iridescence", kpis='[{"label":"营收","value":""}]'),
                         jsonld_check=False)
    assert "animated.invalid_summary_kpi" in empty_value
    empty_list = _codes(_animated_html("iridescence", kpis="[]"), jsonld_check=False)
    assert "animated.missing_summary_kpis" in empty_list


def test_animated_rejects_external_font_origin():
    font = '<link href="https://fonts.googleapis.com/css2?family=X" rel="stylesheet">'
    codes = _codes(_animated_html("iridescence", body=font), jsonld_check=False)
    assert "animated.external_font" in codes


def test_animated_webgl_fallback_is_colour_agnostic():
    """Brand-tinted fallback must pass; a missing assignment must not."""
    branded = _animated_html("iridescence").replace(
        "linear-gradient(135deg,#cfe0ff,#f0f6ff)", "linear-gradient(135deg,#ffd9da,#fff5f5)")
    assert validate_html_text(branded)["status"] == "valid"
    dropped = _animated_html("iridescence").replace(
        "if(!gl){canvas.style.background='linear-gradient(135deg,#cfe0ff,#f0f6ff)';}", "")
    assert "animated.missing_webgl_fallback" in _codes(dropped, jsonld_check=False)


def test_standard_shell_ids_cannot_be_satisfied_from_a_comment():
    html = """
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.24.0" data-theme="minimal">
<head><style>/* Theme: minimal */ --font-sans: x; body { font-family: var(--font-sans) }</style></head>
<body>
<script type="application/json" id="report-summary">{"title":"T","sections":[],"kpis":[]}</script>
<!-- id="toc-toggle-btn" id="toc-sidebar" id="card-mode-btn" id="sc-overlay"
     id="edit-hotzone" id="edit-toggle" id="export-btn" id="export-menu"
     id="export-print" id="export-png-desktop" id="export-png-mobile" id="export-im-share" -->
</body></html>
""".strip()
    assert "shell.missing_id" in _codes(html, jsonld_check=False)


def test_shipped_animated_examples_pass_the_gate():
    for name in ("tesla-q2-2026.html", "tesla-q2-2026-scrollytelling.html"):
        path = ROOT / "examples" / "zh" / name
        report = validate_html_text(path.read_text(encoding="utf-8"))
        assert report["status"] == "valid", (name, report["findings"])


def test_forest_editorial_theme_fingerprint():
    """Built-in theme CSS must survive assembly; the marker set is the contract."""
    theme_css = (ROOT / "templates" / "themes" / "forest-editorial.css").read_text(encoding="utf-8")
    html = f"""
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.24.0" data-theme="forest-editorial">
<head><style>{theme_css}</style></head>
<body>
<script type="application/json" id="report-summary">{{"title":"T","sections":[],"kpis":[]}}</script>
</body>
</html>
""".strip()
    report = validate_html_text(html, standard_shell=False, jsonld_check=False)
    assert report["status"] == "valid", report["findings"]


def test_forest_editorial_fingerprint_rejects_hand_rolled_css():
    html = """
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.24.0" data-theme="forest-editorial">
<head><style>body { background: #f5f7f3; font-family: sans-serif; }</style></head>
<body>
<script type="application/json" id="report-summary">{"title":"T","sections":[],"kpis":[]}</script>
</body>
</html>
""".strip()
    codes = {f["code"] for f in validate_html_text(html, standard_shell=False, jsonld_check=False)["findings"]}
    assert "theme.fingerprint_mismatch" in codes
