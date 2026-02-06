"""Run setup smoke test.

Assumptions:
* MLflow server is already running and reachable at configs/mlflow.yaml tracking_uri.
* Optuna storage is sqlite as configured in configs/optuna.yaml.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Final

import mlflow
import optuna
import yaml
from mlflow.tracking import MlflowClient

from configs.mlflow_config import MlflowServiceConfig
from configs.optuna_config import OptunaRunnerConfig

LOGGER: Final[logging.Logger] = logging.getLogger(__name__)

SMOKE_NAME: Final[str] = "setup_smoke_test"
N_TRIALS: Final[int] = 1

# TODO: remove REPO_ROOT
REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> Any:
    """Load a YAML configuration file."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MLflow + Optuna setup smoke test.")
    parser.add_argument("--mlflow-config", default="configs/mlflow.yaml")
    parser.add_argument("--optuna-config", default="configs/optuna.yaml")
    return parser.parse_args(argv)


def _mlflow_backend_store_uri(cfg: MlflowServiceConfig) -> str:
    if cfg.backend_kind != "sqlite":
        raise ValueError(f"Unsupported MLflow backend_kind for smoke test: {cfg.backend_kind}")
    return f"sqlite:///{cfg.backend_path.as_posix()}"


def _require_mlflow_server(tracking_uri: str) -> MlflowClient:
    client = MlflowClient(tracking_uri=tracking_uri)
    try:
        _ = client.search_experiments(max_results=1)
    except Exception as exc:
        raise RuntimeError(
            "Could not reach MLflow tracking server. Start it first (see README.md). "
            f"tracking_uri={tracking_uri}"
        ) from exc
    return client


def _write_artifact(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run_optuna_trial(optuna_cfg: OptunaRunnerConfig, mlflow_cfg: MlflowServiceConfig) -> str:
    mlflow.set_tracking_uri(mlflow_cfg.tracking_uri)
    mlflow.set_experiment(SMOKE_NAME)

    sampler = optuna.samplers.RandomSampler(seed=optuna_cfg.study.seed)
    study = optuna.create_study(
        study_name=SMOKE_NAME,
        storage=optuna_cfg.storage.uri,
        direction="minimize",
        load_if_exists=optuna_cfg.study.load_if_exists,
        sampler=sampler,
    )

    def objective(trial: optuna.Trial) -> float:
        x = trial.suggest_float("x", 0.0, 1.0)
        y = trial.suggest_int("y", 0, 10)
        value = float(x) + float(y) / 100.0

        with mlflow.start_run(run_name=f"trial_{trial.number}"):
            mlflow.log_param("x", x)
            mlflow.log_param("y", y)
            mlflow.log_metric("objective", value)
            mlflow.set_tag("purpose", SMOKE_NAME)
            mlflow.set_tag("optuna_trial_number", str(trial.number))

            artifact_path = REPO_ROOT / "output" / SMOKE_NAME / "smoke_test_artifact.json"
            _write_artifact(
                artifact_path,
                {
                    "experiment": SMOKE_NAME,
                    "study": SMOKE_NAME,
                    "trial_number": trial.number,
                    "objective": value,
                },
            )
            mlflow.log_artifact(str(artifact_path), artifact_path=SMOKE_NAME)

            active = mlflow.active_run()
            if active is None:
                raise RuntimeError("MLflow active_run() returned None inside run context")
            trial.set_user_attr("mlflow_run_id", active.info.run_id)

        return value

    study.optimize(objective, n_trials=N_TRIALS)

    # Return the run_id we stored on the (only) completed trial.
    complete = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    if not complete:
        raise RuntimeError("Optuna study exists, but has no COMPLETE trials")
    run_id = complete[-1].user_attrs.get("mlflow_run_id")
    if not run_id:
        raise RuntimeError("Optuna trial missing expected user attr: mlflow_run_id")
    return str(run_id)


def _verify_optuna(optuna_cfg: OptunaRunnerConfig) -> None:
    db_path = (REPO_ROOT / optuna_cfg.storage.dir_path / optuna_cfg.storage.db_name).resolve()
    if not db_path.exists():
        raise RuntimeError(f"Optuna sqlite DB not found: {db_path}")

    study = optuna.load_study(study_name=SMOKE_NAME, storage=optuna_cfg.storage.uri)
    complete = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    if not complete:
        raise RuntimeError("Optuna study exists, but has no COMPLETE trials")


def _verify_mlflow(
    mlflow_cfg: MlflowServiceConfig, client: MlflowClient, expected_run_id: str
) -> None:
    if mlflow_cfg.backend_kind == "sqlite":
        db_path = (REPO_ROOT / mlflow_cfg.backend_path).resolve()
        if not db_path.exists():
            raise RuntimeError(f"MLflow sqlite backend file not found: {db_path}")

    experiment = client.get_experiment_by_name(SMOKE_NAME)
    if experiment is None:
        raise RuntimeError(f"MLflow experiment not found: {SMOKE_NAME}")

    run = client.get_run(expected_run_id)
    if run.info.experiment_id != experiment.experiment_id:
        raise RuntimeError(
            "MLflow run exists, but is not under the expected experiment. "
            f"expected_experiment={experiment.experiment_id} "
            f"actual_experiment={run.info.experiment_id}"
        )

    if run.data.tags.get("purpose") != SMOKE_NAME:
        raise RuntimeError(f"MLflow run missing expected tag: purpose={SMOKE_NAME}")

    for key in ["x", "y"]:
        if key not in run.data.params:
            raise RuntimeError(f"MLflow run missing expected param: {key}")
    if "objective" not in run.data.metrics:
        raise RuntimeError("MLflow run missing expected metric: objective")

    artifacts = client.list_artifacts(run.info.run_id, path=SMOKE_NAME)
    if not artifacts:
        raise RuntimeError(f"MLflow run missing expected artifact path: {SMOKE_NAME}/")


def _run_test(argv: list[str]) -> int:
    """Run smoke test and return exit code."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        args = _parse_args(argv)

        mlflow_cfg = MlflowServiceConfig.model_validate(load_config(Path(args.mlflow_config)))
        optuna_cfg = OptunaRunnerConfig.model_validate(load_config(Path(args.optuna_config)))

        # Encourage config alignment: backend uri computed from config should
        # match how the server was started.
        _ = _mlflow_backend_store_uri(mlflow_cfg)

        client = _require_mlflow_server(mlflow_cfg.tracking_uri)

        expected_run_id = _run_optuna_trial(optuna_cfg, mlflow_cfg)

        _verify_optuna(optuna_cfg)
        _verify_mlflow(mlflow_cfg, client, expected_run_id)

    except Exception as exc:  # pylint: disable=broad-exception-caught
        LOGGER.error("Smoke test FAILED: %s", exc)
        return 1

    LOGGER.info("Smoke test OK")
    LOGGER.info("MLflow: %s (experiment=%s)", mlflow_cfg.tracking_uri, SMOKE_NAME)
    LOGGER.info("Optuna: %s (study=%s)", optuna_cfg.storage.uri, SMOKE_NAME)
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_test(sys.argv[1:]))
