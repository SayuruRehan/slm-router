# TRACER Baseline Runbook

<!-- TRACER-30: canonicalize the Qwen and Gemma viewer/runner workflow. -->
<!-- TRACER-31: provide one reproducible command for the paired 20-sample baseline. -->

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,viewer]"
```

Ensure Ollama is running and the two configured models are present:

```bash
ollama pull qwen2.5-coder:1.5b
ollama pull gemma3:4b
```

The Docker validator uses `python:3.11-slim` when executable tests are available. Keeping the image pre-pulled avoids image-download time being confused with candidate execution time:

```bash
docker pull python:3.11-slim
```

## Validate the frozen experiment configuration

```bash
tracer-baseline --config configs/qwen25_coder_baseline.yaml --dry-run
tracer-baseline --config configs/gemma3_baseline.yaml --dry-run
```

Both dry runs must show the same 20 manifest entries.

## Run TRACER-31 as one paired experiment

```bash
python scripts/run_tracer31_baselines.py
```

The script runs both models through the canonical `tracer-baseline` CLI and refuses to complete unless:

- both commands exit successfully;
- both standardized JSON outputs are newly created or refreshed;
- each output contains exactly 20 records;
- the ordered sample identities are identical;
- required model, token, response, validation, and validator-provenance fields are present.

After successful completion it writes:

```text
results/baselines/tracer31_run_manifest.json
```

This file records the shared sample identities and the host OS/hardware context for the paired run.

## Standardized outputs

Qwen:

```text
results/baselines/qwen25_coder_records.json
results/baselines/qwen25_coder_records.csv
results/baselines/qwen25_coder_summary.json
```

Gemma:

```text
results/baselines/gemma3_records.json
results/baselines/gemma3_records.csv
results/baselines/gemma3_summary.json
```

## Viewers

Qwen:

```bash
streamlit run code/sula/app.py
```

Gemma:

```bash
streamlit run code/lithma/PoCs/debugbench-gemma-poc/app.py
```

Both viewers call the canonical shared runner. A viewer reports success only when its expected standardized result file has actually been created or refreshed.

The older `code/sula/run.py` and `code/lithma/PoCs/debugbench-gemma-poc/run_poc.py` commands are retained only as compatibility wrappers. They delegate to `tracer-baseline` and no longer create conflicting legacy `results.json` files.
