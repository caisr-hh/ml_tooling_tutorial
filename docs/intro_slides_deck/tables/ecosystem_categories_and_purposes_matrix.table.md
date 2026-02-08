---
puppeteer:
  width: "16in"
  height: "9in"
  scale: 0.8
  printBackground: true
  margin:
    top: "10mm"
    right: "10mm"
    bottom: "10mm"
    left: "10mm"
---

| Category | Answers | Typical capabilities | Non-goals |
| --- | --- | --- | --- |
| Code versioning (Git) | * Which code snapshot did we use? | * history, diff, review, branching, tags<br/>* code provenance for papers and experiments | * does not version large data well<br/>* does not record "runs" or produced artifacts by itself |
| Data versioning and lineage (DVC, lakeFS, etc.) | * Which dataset snapshot did we use?<br/>* Which derived artifacts depend on which inputs? | * data snapshots / versions (often stored outside git)<br/>* lineage via declared deps/outs<br/>* reproducible data pipelines in terms of file dependencies<br/>* stage skip via cache and "nothing changed" detection (DVC-style) | * not a full experiment tracker UI<br/>* not a scheduler/queue/retry system (beyond simple stage execution) |
| Environment capture (conda/mamba, lockfiles) | * Which exact dependencies made this run work? | * pinned packages / versions<br/>* exportable environment spec (env.yml / lockfile)<br/>* reduces environment drift across machines | * does not track runs, metrics, or artifacts |
| Training frameworks (Lightning, HF Trainer, etc.) | * How do we write training loops faster and more consistently? | * training loop abstractions<br/>* standard callbacks, logging hooks<br/>* multi-GPU / mixed precision conveniences (depending on framework) | * not experiment tracking by itself<br/>* not orchestration by itself<br/>* not data versioning |
| Experiment tracking (MLflow, W&B, etc.) | * Which run produced this result?<br/>* What parameters, metrics, and artifacts did it generate? | * run records: params, metrics, tags<br/>* artifact logging: plots, tables, models, reports<br/>* comparison: search, filter, compare runs<br/>* provenance links (to code/config/data references) if you log them | * not HPO search engine (though it can integrate with one)<br/>* not orchestration/scheduling (though it can be triggered from one) |
| HPO optimization (Optuna, Ray Tune, etc.) | * How do we search the hyperparameter and design space systematically? | * define objective functions<br/>* search algorithms (samplers), pruning, early stopping<br/>* study analysis and visualizations<br/>* parallel trial execution (varies by tool and setup) | * does not guarantee provenance unless paired with tracking/versioning<br/>* does not replace broader evaluation surface (metrics beyond the objective) |
| Orchestration (Prefect, Dagster, Airflow, Argo/KFP) | * How do we run the workflow reliably and repeatedly, at scale? | * scheduling and triggers<br/>* retries, backoff, timeouts<br/>* concurrency / queues / distributed execution primitives<br/>* task caching / stage skip (orchestrator-style), idempotency patterns<br/>* observability of workflow runs (logs, states) | * not a tracker unless you log to a tracker<br/>* not a data versioning system (though it can call one) |
