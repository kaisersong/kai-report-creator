# Report-Creator Eval Gap Report

Date: 2026-05-28

## Baseline Status

| Metric | Value |
|--------|-------|
| Fixture eval (6 cases) | 100/100 all pass |
| Unit tests | 215 pass |
| Scorer version | rubric-optional policy applied |

## Changes Applied

### 1. Rubric-Optional Policy (scorer fix)

**Problem**: `score_style` penalized live runs for missing `style-rubric.json`, but SKILL.md never instructs agents to produce one. This caused `eval_complete=False` and artificial -10 penalty on every live run.

**Fix**: When no rubric is available, scale the base style score (0-15) up to 25 instead of penalizing:
```python
score = round(score * 25 / 15) if score > 0 else 0
```

**Impact**: Live runs can now achieve 100/100 without a rubric file. Fixtures with rubrics still use the rubric score.

### 2. Test Update

Renamed `test_positive_case_without_style_rubric_is_eval_incomplete` to `test_positive_case_without_style_rubric_scales_base_score`. Now asserts: returncode=0, style=25, total=100, passed=True, eval_complete=True.

## Gaps Identified (No Code Changes Needed)

### Gap A: Scorer Does Not Execute Quality Gate

The scorer checks `metrics.skill_evidence.get("html_quality_gate_observed")` from the trace — it does **not** invoke `scripts/html_quality_gate.py` itself. This means:

- Fixture traces can claim `html_quality_gate_observed: true` without the HTML actually passing the gate
- The actual fixture HTML (`tests/fixtures/skill_eval_explicit_generate.html`) fails the CLI gate (missing required shell IDs)
- This is acceptable for unit-testing the scorer, but means fixture eval does not validate HTML quality

**Recommendation**: No change. The fixture runner tests scorer logic in isolation. Live eval (agent actually runs the gate) is the correct layer for end-to-end HTML validation.

### Gap B: No Live Runner Without Codex

The `--run-live` mode shells out to `codex exec`. Per user requirement "eval不能依赖codex", a live runner path that works with other agents (e.g., Qoder CLI, OpenAI API direct) does not exist yet.

**Recommendation**: Add a `--runner qoder` or `--runner api` mode in future if live eval is needed. For now, the `--normalized-trace` mode allows scoring any agent's output as long as it's normalized to `normalized-v1` schema.

### Gap C: Efficiency Budgets Are Generous

Current budgets (e.g., 90K input tokens, 25K output, 240s wall) are ~2.5x the fixture ideal path. This is intentional headroom for real agents that may retry or explore.

**Recommendation**: No change. Tighten only after collecting real agent traces.

### Gap D: Style Rubric Generation Responsibility

Style rubrics exist as fixtures but no agent or script produces them during live runs. The rubric schema (6 checks: async_readability, visual_rhythm, evidence_fidelity, no_ai_slop, theme_appropriateness, decision_support) is complex.

**Recommendation**: Style rubrics should be produced by a separate evaluation pass (LLM-as-judge or human review), not by the skill agent itself. The rubric-optional policy ensures eval still works without them.

## Eval Architecture Summary

```
Fixture Runner (pytest/CI):
  Normalized JSON traces → Scorer → 100/100 baseline
  Purpose: Validate scorer logic, regression-test scoring rules

Live Runner (agent execution):
  Agent + Prompt → Raw trace → Normalize → Scorer
  Purpose: Measure actual agent capability
  Status: Only codex runner implemented; --normalized-trace accepts any source

Scoring Dimensions:
  Outcome (25): HTML exists + quality_gate_observed + report-summary + no raw IR
  Process (25): SKILL.md read + route refs + report_flow + guard + quality_gate
  Style   (25): Theme match + report-summary + no placeholders (+ optional rubric)
  Efficiency(25): Within budget on commands, tokens, wall time
```

## Conclusion

The report-creator eval infrastructure is functional and correctly validates the scoring pipeline. The rubric-optional fix aligns with the principle "SKILL.md只负责用户使用逻辑" — the scorer no longer penalizes agents for not producing evaluation artifacts that aren't part of the user-facing workflow. No further code changes are needed at this stage.
