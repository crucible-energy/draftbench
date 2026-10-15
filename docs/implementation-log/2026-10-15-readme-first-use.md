# Draftbench README first-use navigation

Owner: organization README mission, Reviewer Renata (`candidate_custody_review`).
Branch: `codex/readme-first-use`.
Source: [fork main `93e5e11e`](https://github.com/crucible-energy/draftbench/tree/93e5e11e5c934047a3e72b976762e5f93ae0f491).
Mission authority: Sam's standing organization README program; no separate
repository issue was opened. The [prior README](../history/2026-10-15-root-readme.md)
is the historical documentation source. No prior implementation log exists on
this baseline.

This independently owned log adopts the focused log procedure from
[Kaizen `4ca2672d`](https://github.com/crucible-energy/kaizen/blob/4ca2672d97ffe34d9a7d9a4df3d6f8b6c93c8b51/docs/mission-log-procedure.md)
within the existing contribution workflow. Final frozen validation belongs in
external receipts and the PR, so reporting a pass does not change the candidate.

## User Experience Findings

### October 15, 2026

- The original quick start uses nonexistent `--url` and `--requests` arguments
  and omits the required model ID. The current front door documents the retained
  parser's `--base-url`, `--model`, `--runs` and explicit prompt form.
- A useful first step should not require a running model, backend installation
  or hardware allocation. The chart-only path reads a bundled result and writes
  a deliberately named HTML file; its Python imports still require `requests`.
- The sweep's `backend` field is output metadata, while its execution always
  uses `LlamaCppBackend`. Standalone adapters do not prove current external
  backend qualification. Throughput's streamed-chunk fallback is approximate.
- Bare-name llama.cpp discovery and a subsequent `isfile` check can disagree.
  The docs recommend an explicit absolute binary path. This source limitation
  is recorded, not repaired or claimed fixed by the docs change.

## Engineering Decisions

### October 15, 2026

- Reuse the independently pinned preassessment, then verify fresh fork main and
  its source hashes before admission. Select the Crucible fork as the single
  intended push destination; local `origin` belongs to the upstream repository.
- Use an isolated second docs carrier. Preserve the nested primary's original
  branch, HEAD, index, staged and working patches, untracked source/results and
  private ignored state. Historical OpenCode metadata explains the source lane;
  its current active owner is not established, and cleanliness or missing task
  metadata is not treated as authority to take it over.
- Keep the current README concise and preserve the entire previous text beneath
  a dated historical header linked to the exact original Git blob. No original
  relative Markdown links need rebasing. No tracked baseline Markdown inbound
  README fragment was found; current heading changes are intentional and the
  historical headings remain accessible in the companion.
- Preserve upstream attribution, MIT licensing, original results and existing
  Python source. Do not turn documentation repair into a language migration,
  model benchmark, backend installation or external qualification.

## Known Limitations

### October 15, 2026

- Help and chart rendering do not establish inference correctness, answer
  quality, hardware performance, server cleanup, target/draft compatibility or
  live backend support. No new model or provider operation is part of this slice.
- Python and `requests` have no pinned support matrix/lock in this baseline;
  exact local validation versions are recorded externally. The repository has
  no dedicated test suite, Makefile or active installed delivery hook at
  admission. New source work still needs appropriate validation.
- The separate dirty Qwen3.5 source lane and its README changes remain protected.
  Their integration needs source-owner review against fresh main, relevant
  executable proof and normal publication. This documentation does not adopt or
  qualify those experiments; the original source/index state remains recoverable.
- Historical generic gains and recommendations remain complete as dated source
  narrative, not universal guidance. The chunk-count fallback and llama.cpp
  path-discovery limitation remain source recovery items for a bounded owning
  repair. No measured cost, token or time savings are claimed.
