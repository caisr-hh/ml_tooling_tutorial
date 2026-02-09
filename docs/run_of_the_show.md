# Run of the show

## Agenda

- we haven't really timed all the sessions
- these are rough estimates, we'll do our best to stick to it.

| time | what |
| ---- | ---- |
| 09:00 - 09:10 | <i class="fa fa-sun"></i> good-morning |
| 09:10 - 09:30 | introduction; motivation and tooling |
| 09:30 - 11:20 | guided build; MLflow + Optuna |
| **11:20 - 11:30** | <i class="fa fa-mug-hot"></i> break |
| 11:30 - 12:00 | guided tour; DVC + Prefect |
| 12:00 - 12:10 | short talk: Scaling ML Observability |
| **12:10 - 13:10** | <i class="fa fa-utensils"></i> lunch |
| 13:10 - 15:15 | projects |
| **13:00 - 15:15** | <i class="fa fa-mug-hot"></i> break |
| 15:20 - 16:00 | share your findings |

## Resource

- entry point: [https://github.com/caisr-hh/ml_tooling_tutorial](https://github.com/caisr-hh/ml_tooling_tutorial)
- hands on : [https://github.com/caisr-hh/handson_mlflow_optuna](https://github.com/caisr-hh/handson_mlflow_optuna)
- demos: [https://github.com/caisr-hh/dvc_prefect_demo](https://github.com/caisr-hh/dvc_prefect_demo)

## Note

- This is the first run of this event, forgive the shortcomings
    - take note, we would appreciate feedbacks
- By no means or measure we consider ourselves expert!
    - We are sharing our experience hoping it would excite you. Also we hope by
      slightly gentling the first bump of the learning curve, adoption could
      become easier for you.
- Material for the DVC+Prefect demos have been curated with help from ChatGPT

## Projects

An opportunity to explore the topics and tools further.

- build something simple:
    - **pick a problem from your own back-burner** tha would be suitably solved by what you learned today.
    - [**MLflow**] single MLflow service on a remote host, shared and used by multiple users interacting with same/different MLflow experiments.
    - [**MLflow**] a simple webApp (e.g. using streamlit) with a ML model as backend, run experiment and deploy new models with MLflow to the webapp.
    - [**MLflow**] robust and rich MLflow artifact and detail logging. (Rich artifact helpers: `mlflow.log_figure`, `mlflow.log_image`,  `mlflow.log_text`, `mlflow.log_dict`, `mlflow.log_table`. Datasets / lineage: `mlflow.log_input` , `mlflow.log_inputs`, `mlflow.log_outputs`. Guard each critical artifact explicitly)
    - [**MLflow**] MLflow + gitlab: gitlab has built-in support for MLflow
    - [**MLflow**] dangling MLflow runs: when process is killed mid-run a "MLflow context", the run could be left dangling and never finish, because the context in the scope of `with` never closes!
        - is there a need to clean up, how to detect, and how to declutter?
    - [**Optuna**] dangling Optuna trials: similarly Optuna cannot identify when a process is killed and leaves them as "unfinished"!
        - is there a need to clean up, how to detect, and how to declutter?
    - [**Optuna**] compounding hyper params (e.g. changing `hidden_dims` in a NN/MLP means that the values suggested by Optuna for some layers are irrelevant, and Optuna does not have a clean way of treating the number of nodes per layer as a hyper-param).
        - How to treat parameter importance in such cases
    - [**Optuna**] pruning with multi-objectives
    - [**Optuna**] distributed run
    - [**MLflow, Optuna**] MLflow run URL added to Optuna trials in Optuna Visualization, so that we can jump from Optuna visualization directly to corresponding run on the MLFlow UI 
    - [**MLflow, Optuna**] notification for when study/experiment stopped or finished, etc.
    - [**Misc**] inference optimization (e.g., quantization, ONNX/TensorRT export)
- Or, if you don't want to code, contemplate! Run a round table discussion (but not alone by yourself)!
