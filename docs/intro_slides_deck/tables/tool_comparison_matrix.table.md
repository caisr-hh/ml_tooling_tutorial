---
puppeteer:
  width: "16in"
  height: "11in"
  scale: 0.9
  printBackground: true
  margin:
    top: "10mm"
    right: "10mm"
    bottom: "10mm"
    left: "10mm"
---

| Tool | Tracking (runs) | Artifacts | Provenance (code/config/data link) | Orchestration (scheduling) | Retries | Parallelism / queues | Stage skip / caching | HPO optimization | Training framework | Versioning (code/data) | Typical deployment | License model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MLflow | X | X | X |  |  |  |  |  |  |  | self-host / local | FOSS |
| Weights and Biases | X | X | (x) |  |  |  |  | (x) |  |  | SaaS / enterprise | Commercial (free tier) |
| TensorBoard | (x) | (x) |  |  |  |  |  |  |  |  | local | FOSS |
| Prefect | (x) |  |  | X | X | X | X |  |  |  | self-host / cloud | Open core |
| Dagster | (x) |  | (x) | X | (x) | X | X |  |  |  | self-host / cloud | Open core |
| Airflow |  |  |  | X | (x) | X | (x) |  |  |  | self-host / managed | FOSS |
| Argo Workflows |  |  |  | X | (x) | X | (x) |  |  |  | Kubernetes | FOSS |
| Kubeflow Pipelines |  |  | (x) | X | (x) | X | (x) | (x) |  |  | Kubernetes | FOSS |
| Optuna |  |  |  |  |  | (x) |  | X |  |  | local / service-backed | FOSS |
| Ray Tune |  |  |  | (x) | (x) | X | (x) | X |  |  | Ray cluster | FOSS |
| DVC |  | (x) | X | (x) |  |  | X |  |  | X (data) | local / remote storage | FOSS |
| Git |  |  | X (code) |  |  |  |  |  |  | X (code) | everywhere | FOSS |
| lakeFS |  |  | X (data) |  |  |  | (x) |  |  | X (data) | service / storage layer | Open core |
| PyTorch Lightning |  | (x) |  |  |  |  |  |  | X |  | library | FOSS |
| Hugging Face Trainer |  | (x) |  |  |  |  |  |  | X |  | library | FOSS |