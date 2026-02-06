.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##### Dev Targets
.PHONY: setup-smoke-test
setup-smoke-test: ## Run a quick end-to-end check that MLflow and Optuna work together.
	@echo "\n=== Running smoke test to check MLflow/Optuna ==="
	@python -m scripts.setup_smoke_test

.PHONY: formatter
formatter: ## Check code formatting.
	@echo "\n=== Checking code formatting ==="
	@black --check .

.PHONY: linter
linter: ## Run the linter.
	@echo "\n=== Linting Python files (all) ==="
	@pylint $(shell git ls-files '*.py')

MYPY_OPTS = --install-types --non-interactive --explicit-package-bases --config-file=pyproject.toml --show-error-codes

.PHONY: type-check
type-check: ## Run static type checking.
	@echo "\n=== Running type checks (all) ==="
	@mypy $(MYPY_OPTS) .

.PHONY: code-quality
code-quality: ## Run the main code-quality checks (formatting, linting, typing).
	-@$(MAKE) formatter
	-@$(MAKE) type-check
	-@$(MAKE) linter

##### Env targets
.PHONY: ensure-mamba
ensure-mamba: ## Ensure mamba is installed in the conda base environment.
	@conda list -n base mamba 1>/dev/null 2>&1 \
		&& echo "mamba already installed in conda base." \
		|| (echo "Installing mamba into conda base..." && conda install -n base -c conda-forge -y mamba)

.PHONY: create-env
create-env: ensure-mamba ## Create the conda environment for this repo.
	@echo "\n=== Creating conda virtual environment (using mamba) ==="
	ulimit -n 262144 && mamba env create -f environment.yaml

# syncs with environment.yaml
# does not update existing environment even if it is outdated and ignores lock file if it exists
.PHONY: update-env
update-env: ensure-mamba ## Update the conda environment to match the repo dependencies.
	@echo "\n=== Updating conda virtual environment (using mamba) ==="
	ulimit -n 262144 && mamba env update -f environment.yaml

##### MLflow targets
# NOTE: these should match configs/mlflow.yaml
MLFLOW_HOST          ?= 127.0.0.1
MLFLOW_PORT          ?= 5000
MLFLOW_ARTIFACT_ROOT ?= $(PWD)/mlruns
MLFLOW_DB_PATH       ?= $(MLFLOW_ARTIFACT_ROOT)/mlflow.db
MLFLOW_BACKEND_URI   ?= sqlite:///$(MLFLOW_DB_PATH)
MLFLOW_WORKERS       ?= 2
MLFLOW_TIMEOUT       ?= 60

.PHONY: mlflow-start
mlflow-start: ## Start the MLflow tracking server.
	@echo "\n=== Starting MLflow Tracking Server (DB backend) ==="
	nohup mlflow server \
		--backend-store-uri $(MLFLOW_BACKEND_URI) \
		--default-artifact-root file:$(MLFLOW_ARTIFACT_ROOT) \
		--host $(MLFLOW_HOST) \
		--port $(MLFLOW_PORT) \
		--workers $(MLFLOW_WORKERS) \
		--gunicorn-opts="--timeout $(MLFLOW_TIMEOUT) --worker-tmp-dir /dev/shm" \
		&

.PHONY: mlflow-stop
mlflow-stop: ## Stop the MLflow tracking server.
	@fuser -k $(MLFLOW_PORT)/tcp || true

.PHONY: mlflow-status
mlflow-status: ## Check whether the MLflow server is reachable.
	@curl -fsS "http://$(MLFLOW_HOST):$(MLFLOW_PORT)/" >/dev/null && \
	  echo "MLflow server is UP at http://$(MLFLOW_HOST):$(MLFLOW_PORT)/" || \
	  echo "MLflow server is DOWN"

##### Optuna targets
# NOTE: these should match configs/optuna.yaml
OPTUNA_HOST            ?= 127.0.0.1
OPTUNA_PORT            ?= 8080
OPTUNA_STORAGE_PATH    ?= $(PWD)/optuna_studies
OPTUNA_STORAGE_DB_PATH ?= $(OPTUNA_STORAGE_PATH)/optuna.db
OPTUNA_STORAGE_URI     ?= sqlite:///$(OPTUNA_STORAGE_DB_PATH)
OPTUNA_STORAGE_CLASS   ?= "RDBStorage"

.PHONY: optuna-dashboard-start
optuna-dashboard-start: ## Start the Optuna dashboard.
	@echo "\n=== Starting Optuna Dashboard with custom config ==="
	nohup optuna-dashboard \
	--host ${OPTUNA_HOST} \
	--port ${OPTUNA_PORT} \
	--storage-class ${OPTUNA_STORAGE_CLASS} ${OPTUNA_STORAGE_URI} \
	&

.PHONY: optuna-dashboard-stop
optuna-dashboard-stop: ## Stop the Optuna dashboard.
	@echo "Stopping Optuna Dashboard on port $(OPTUNA_PORT)"
	@fuser -k $(OPTUNA_PORT)/tcp || true

.PHONY: optuna-dashboard-status
optuna-dashboard-status: ## Check whether the Optuna dashboard is reachable.
	@curl -fsS "http://$(OPTUNA_HOST):$(OPTUNA_PORT)/" >/dev/null && \
	  echo "Optuna Dashboard is UP at http://$(OPTUNA_HOST):$(OPTUNA_PORT)/" || \
	  echo "Optuna Dashboard is DOWN"
