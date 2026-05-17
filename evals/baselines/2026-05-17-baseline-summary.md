# 2026-05-17 Eval Baseline

This baseline captures the current `kai-report-creator` eval state before
future skill changes.

## Saved Files

- `2026-05-17-skill-evals-fixture.json`
- `2026-05-17-skill-evals-codex-live.json`
- `2026-05-17-report-evals.json`
- `2026-05-17-late-context-evals.json`

## Captured-Run Skill Evals: Fixture Runner

Fixture runner baseline is deterministic and should stay green unless the
scorer, prompt manifest, or fixture metrics intentionally change.

| Case | Total | Outcome | Process | Style | Efficiency | Pass |
|------|-------|---------|---------|-------|------------|------|
| explicit-generate | 90 | 25 | 25 | 15 | 25 | yes |
| implicit-weekly-progress | 90 | 25 | 25 | 15 | 25 | yes |
| contextual-research | 90 | 25 | 25 | 15 | 25 | yes |
| boundary-blueprint-report | 90 | 25 | 25 | 15 | 25 | yes |
| negative-slide-deck | 100 | 25 | 25 | 25 | 25 | yes |
| negative-html-export | 100 | 25 | 25 | 25 | 25 | yes |

Summary:

- Total: 6
- Passed: 6
- Failed: 0
- Average score: 93.33
- Average category scores: Outcome 25.0, Process 25.0, Style 18.33, Efficiency 25.0

The positive cases intentionally score Style 15/25 because no
model-assisted `style-rubric.json` is present. The scorer records
`style.rubric_missing` instead of treating fixture mode as a full style grade.

## Captured-Run Skill Evals: Codex Live Runner

Live runner baseline records the current behavior of `codex exec` under the
harness. It is not green today.

This file was refreshed after runner hardening: the harness now passes the eval
prompt through stdin with `codex exec ... -`, parses partial JSONL traces on
timeout, and treats incomplete runs as failures. That makes this baseline more
pessimistic than the first smoke run, but it is a better comparison point:
negative controls can no longer pass just because the runner timed out before
doing visible harm.

| Case | Total | Outcome | Process | Style | Efficiency | Pass |
|------|-------|---------|---------|-------|------------|------|
| explicit-generate | 82 | 25 | 25 | 15 | 17 | no |
| implicit-weekly-progress | 42 | 0 | 25 | 0 | 17 | no |
| contextual-research | 42 | 0 | 25 | 0 | 17 | no |
| boundary-blueprint-report | 42 | 0 | 25 | 0 | 17 | no |
| negative-slide-deck | 92 | 25 | 25 | 25 | 17 | no |
| negative-html-export | 87 | 25 | 25 | 25 | 12 | no |

Summary:

- Total: 6
- Passed: 0
- Failed: 6
- Average score: 64.5
- Average category scores: Outcome 12.5, Process 25.0, Style 10.83, Efficiency 16.17

Dominant runner warnings:

- All cases timed out at their case wall-time budget (`codex.timeout:120.0s`,
  `codex.timeout:240.0s`, or `codex.timeout:300.0s`) and therefore include
  `runner.run_incomplete`.
- The partial traces show the skill contract and report flow are being read, so
  Process now scores 25/25 across all cases. The live problem is completion and
  routing, not lack of trace observability.
- The `Reading additional input from stdin...` warning is gone after switching
  to explicit stdin prompting with `codex exec ... -`.
- Codex still emits a deprecated hooks warning:
  ``[features].codex_hooks` is deprecated. Use `[features].hooks` instead.`

## Deterministic Report Evals

`2026-05-17-report-evals.json`:

- Total: 3
- Passed: 3
- Failed: 0
- Rubric-ready packets: 3

## Late-Context Evals

`2026-05-17-late-context-evals.json`:

- Total: 3
- Passed: 3
- Failed: 0
- Baseline cases with drift: 3
- Isolated cases with drift: 0
- Baseline total drift fields: 7
- Isolated total drift fields: 0
- Drift reduction: 7

## Re-run Commands

```bash
python3 scripts/run-skill-evals.py --runner fixture --artifact-dir .tmp/baseline-skill-evals-fixture-artifacts --format json --json-out evals/baselines/2026-05-17-skill-evals-fixture.json
python3 scripts/run-skill-evals.py --runner codex --run-live --format json --json-out evals/baselines/2026-05-17-skill-evals-codex-live.json --artifact-dir evals/artifacts/current/skill-runs-baseline-2026-05-17
python3 scripts/run-report-evals.py --root . --format json --json-out evals/baselines/2026-05-17-report-evals.json --packet-dir .tmp/baseline-report-eval-packets
python3 scripts/run-late-context-evals.py --root . --format json --json-out evals/baselines/2026-05-17-late-context-evals.json
```
