# ML Tooling Tutorial

This repo is used in hands-on sessions and demos covering:

* MLflow (tracking) + Optuna (HPO) hands-on: [see here](https://github.com/caisr-hh/handson_mlflow_optuna)
* Prefect (orchestration) + DVC (data versioning) demos: [see here](https://github.com/caisr-hh/dvc_prefect_demo)

## Setup (prerequisites + dependencies)

Follow `docs/setup.md`.

## Start services

All commands below assume:

* you are in the repo root
* your conda environment is activated

### MLflow tracking server

Start MLflow (or use `make mlflow-start`/`make mlflow-stop`):

```bash
# values should match `configs/mlflow.yaml`
mlflow server \
    --backend-store-uri sqlite:///mlruns/mlflow.db \
    --default-artifact-root file:./mlruns \
    --host 127.0.0.1 --port 5000
```

Open the UI at [http://127.0.0.1:5000](http://127.0.0.1:5000).

Stop with `Ctrl+C`.

### Optional: Optuna dashboard

NOTE: Optuna dashboard does not work with an empty sql backend and will fail. Either run the smoke test first (see below), or do:

```bash
python -c "import optuna; optuna.create_study(study_name='setup_smoke_test', storage='sqlite:///optuna_studies/optuna.db', load_if_exists=True)"
```

Start Optuna dashboard (or use `make optuna-dashboard-start`/`make optuna-dashboard-stop`):

```bash
# storage should match `configs/optuna.yaml`
optuna-dashboard \
    --host 127.0.0.1 --port 8080 \
    --storage-class RDBStorage sqlite:///optuna_studies/optuna.db
```

Open the UI at [http://127.0.0.1:8080](http://127.0.0.1:8080).

Stop with `Ctrl+C`.

## Run the smoke test

In a new terminal (or `make setup-smoke-test`):

```bash
python -m scripts.setup_smoke_test
```

This script:

* reads `configs/mlflow.yaml` and `configs/optuna.yaml` by default
* uses MLflow and Optuna APIs to verify that a run/trial was persisted
* exits 0 on success, non-zero on failure

### What to expect (manual UI verification)

Optional, but recommended:

* Open MLflow UI at [http://127.0.0.1:5000](http://127.0.0.1:5000):
    - experiment "setup_smoke_test" exists
    - it contains at least one run
    - the run has params (x, y), metric (objective), and an artifact under `setup_smoke_test/`

* Open Optuna dashboard at [http://127.0.0.1:8080](http://127.0.0.1:8080):
    - study "setup_smoke_test" exists
    - it contains at least one `COMPLETE` trial

## Convenience tips

See `docs/tips.md`.

<details>
<summary>Generate slides from markdown</summary>

```bash
cd docs/intro_slides_deck

pandoc \
    introduction.md -o introduction_slides.pdf \
	-t beamer \
	-f markdown+raw_tex \
	--slide-level=3 \
	--variable aspectratio=169 \
	--variable fontsize=10pt \
    --variable theme=metropolis \
    --highlight-style=tango \
	-H beamer_preamble.tex
```
</details>

## Note

Portions of this code/project were developed with the assistance of ChatGPT (a product of OpenAI).
