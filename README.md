# draftbench

Compare streaming inference throughput and time to first token for the target
and draft model configurations you choose. This Crucible fork of
[alexziskind1/draftbench](https://github.com/alexziskind1/draftbench) retains its
Python tools and [MIT license](LICENSE). Results depend on the endpoint, models,
prompts, settings and hardware; the tools do not evaluate answer quality or prove
a generally optimal draft model.

## Start without running a model

You need Git, Python 3 with `venv` and `pip`, and the declared
[`requests` dependency](requirements.txt). This revision does not declare a
minimum Python version or a tested platform matrix.

```sh
git clone https://github.com/crucible-energy/draftbench.git
cd draftbench
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python bench.py --help
.venv/bin/python sweep.py --results results/m4max-128gb_llamacpp_qwen25-7b.json --chart preview.html --chart-only
```

Setup creates a local environment and normally downloads dependencies from the
package index. Help prints the benchmark arguments. The last command reads a
bundled historical result and creates or overwrites `preview.html`; choose a
different output name if that file matters. It prints `Chart saved to
preview.html` without starting a server, loading a model or sending inference
requests. Open the HTML in a browser to explore the charts; viewing it fetches
Plotly from a CDN. Chart generation itself does not fetch Plotly. `requests` is
still needed because the chart CLI imports the benchmark and server modules.

## Choose a workflow

| Entry point | Current behavior and effects |
| --- | --- |
| [`bench.py`](bench.py) | Sends streaming chat requests to one or two already running OpenAI-compatible endpoints; prints timing and throughput summaries. Does not launch a server or save result JSON. |
| [`server.py`](server.py) | Standalone adapters launch llama.cpp or vLLM, or connect to an existing LM Studio server. Backend software, models and compatible external CLI flags must be arranged separately. |
| [`sweep.py`](sweep.py) | Launches llama.cpp for baseline and target/draft combinations, saves JSON incrementally, resumes successful label pairs and generates charts. The config's `backend` field labels output; it does not select vLLM or LM Studio execution. |
| `sweep.py --chart-only` | Reads existing JSON and writes HTML. This is the first-use path above. |

Inspect the interfaces locally before choosing an operation:

```sh
.venv/bin/python server.py --help
.venv/bin/python sweep.py --help
```

### Benchmark an existing endpoint

After separately arranging an endpoint and confirming its served model ID:

```sh
.venv/bin/python bench.py --base-url http://127.0.0.1:8080/v1 --model YOUR_SERVED_MODEL_ID --runs 1 --prompt 'Write one short sentence.' --max-tokens 32
```

This performs inference: it sends the supplied prompt and requests up to 32
completion tokens, with retries if the endpoint returns a loading response
(503). Replace the model placeholder and base URL for your endpoint. A second
endpoint can be selected with `--compare-url` and `--compare-model`; see
`bench.py --help` for the complete interface. No endpoint or backend readiness
is established by the chart-only example.

For an automatic sweep, adapt [`configs/example_sweep.json`](configs/example_sweep.json)
with actual target/draft GGUF paths, settings and an explicit absolute
`settings.llama_bin` path. The current launcher may discover a bare name on
`PATH` but then reject it with a filesystem check. Arrange sufficient memory,
disk and a free port before starting a sweep. It starts and stops a server,
performs inference, writes result/chart files and uses a temporary server log;
it does not download model files. The [historical guide](docs/history/2026-10-15-root-readme.md#running-a-sweep)
retains the detailed configuration and chart walkthrough, subject to its dated
corrections.

## Read results with their limits

- [`results/`](results) preserves the original JSON and HTML records. The
  bundled M4 Max/Qwen2.5 records are dated February 5–6, 2026; their gains and
  draft-size recommendations are historical observations, not current hardware
  qualification or forecasts for another setup.
- Throughput uses endpoint-reported completion-token usage when available.
  Otherwise, `bench.py` counts nonempty streamed content chunks, which is an
  approximation rather than a tokenizer count. Do not infer token cost or
  answer quality from that fallback.
- Compare matching prompts, settings and hardware. Chart generation only
  renders the supplied records; it does not validate their measurements.

## Development and history

Read [AGENTS.md](AGENTS.md) before contributing. Current tooling is Python;
organization policy requires Zig for new owned implementation and permits
bounded retained-language repairs. This documentation does not establish a Zig
port or fresh backend/platform qualification.

For a docs-only change, check `git diff --check`, local links and documented
arguments, then run the three help commands and the chart-only smoke above.
This revision has no repository test suite, Makefile or configured delivery
hook. Source or backend changes require their own relevant validation.

The [complete prior README](docs/history/2026-10-15-root-readme.md) preserves the
original explanation, setup recipes, example output, metrics, recommendations
and troubleshooting with pinned provenance. Follow this front door for current
commands and capability boundaries. The
[README mission log](docs/implementation-log/2026-10-15-readme-first-use.md)
records the documentation decisions and known limitations.
