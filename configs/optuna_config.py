"""Optuna Configuration"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel


class StudyConfig(BaseModel):  # pylint: disable=too-few-public-methods
    """Optuna Study configs."""

    study: str
    seed: int  # for sampler
    load_if_exists: bool  # resume and existing study if true


class StorageConfig(BaseModel):
    """Optuna Storage and DB config"""

    dir_path: Path
    db_name: str

    def model_post_init(  # pylint: disable=missing-function-docstring
        self, __context: Any | None = None
    ) -> None:
        self.dir_path.mkdir(parents=True, exist_ok=True)

    @property
    def uri(self) -> str:
        """Storage SQLite DB URI"""
        return f"sqlite:///{self.dir_path}/{self.db_name}"


class OptunaRunnerConfig(BaseModel):  # pylint: disable=too-few-public-methods
    """Configuration of the runner"""

    n_trials: int
    n_jobs: int

    study: StudyConfig
    storage: StorageConfig
