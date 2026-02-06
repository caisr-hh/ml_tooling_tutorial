# Setup

This page covers installing prerequisites, namely Git, Conda and Make
(optional), and dependency management through a conda environment.

## Requirements

You need:

*  convenience; not required)

## Install prerequisites

### Git

Official downloads and install instructions:

- [downloads](https://git-scm.com/downloads)
- [installing
  git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Quick options:

* Linux (Debian/Ubuntu): `sudo apt-get update && sudo apt-get install -y git`
* macOS (Apple Xcode Command Line Tools): `xcode-select --install`
* Windows: Install "[Git for Windows](https://git-scm.com/downloads)" (includes
  Git Bash)  

### Conda

Recommended installer for this repo: Miniforge (conda-forge only).

- [download](https://conda-forge.org/download/)
- [documentation](https://docs.conda.io/)

Verify: `conda --version`

### Make (optional)

Make is used for convenience targets, but everything can be run without it.

Quick options:

* Linux (Debian/Ubuntu): `sudo apt-get update && sudo apt-get install -y make`
* macOS: `xcode-select --install`
* Windows: using WSL2 for a Linux-like shell toolchain is highly recommended.

## Optional tools (used by some make targets)

Some convenience make targets use these command-line tools:

* `curl` (used for *-status targets)
* `fuser` (used for *-stop targets on Linux)
    - Note: `fuser` is not standard on macOS; service stop targets may not work as-is

Linux (Debian/Ubuntu): `sudo apt-get update && sudo apt-get install -y curl psmisc`
macOS: `brew install curl`
Windows: Prefer WSL2 if you want to use the make targets that rely on these tools.

## Clone the repo

From a terminal:

```bash
git clone git@github.com:caisr-hh/ml_tooling_tutorial.git
cd ml_tooling_tutorial
```

All commands below assume you are running from the repo root.

## Create local working directories

* Linux/macOS: `mkdir -p mlruns optuna_studies output`
* Windows (PowerShell): `mkdir mlruns,optuna_studies,output`

## Create and activate the conda environment

Option A: conda (works everywhere)

```bash
conda env create -f environment.yaml
conda activate ml_tooling_tutorial
```

Option B: mamba (faster solver, optional)

```bash
conda install -n base -c conda-forge -y mamba
mamba env create -f environment.yaml
conda activate ml_tooling_tutorial
```

If you already created the environment and want to sync it with
environment.yaml:

```bash
conda env update -f environment.yaml
conda activate ml_tooling_tutorial
```

## Quick sanity checks

In the activated environment:

```bash
python --version
mlflow --version
python -c "import optuna; print(optuna.__version__)"
prefect version
dvc --version
```

## Official documentation

* [Conda](https://docs.conda.io/)
* [MLflow](https://mlflow.org/docs/latest/)
* [Optuna](https://optuna.readthedocs.io/)
* [Prefect](https://docs.prefect.io/)
* [DVC](https://dvc.org/doc)
