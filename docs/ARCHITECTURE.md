# System Architecture

## Overview

The system is organized into a research pipeline and an inference application.

```text
CIC-IoT2023 dataset
        |
        v
Kaggle research notebook
        |
        v
Sampling, cleaning and preprocessing
        |
        v
Feature preparation and stratified split
        |
        v
Random Forest / XGBoost / LightGBM experiments
        |
        v
Evaluation and explainability analysis
        |
        v
Exported 8-class XGBoost model + metadata
        |
        v
Python prediction API
        |
        v
Interactive HTML / CSS / JavaScript dashboard
```

## Main components

### Research layer

`notebooks/IoT_Attack_Detection_v2.ipynb` contains the dataset preparation, experiments, metrics, and explainability workflow.

### Export layer

`scripts/export_web_files.py` prepares the model and demonstration artifacts for the web application.

### Inference layer

`web/api/predict.py` loads the model and metadata, validates incoming feature rows, arranges columns in the expected feature order, and returns predictions and probabilities.

### Presentation layer

`web/public/index.html` provides the user interface. It calls the API for inference and uses the demonstration dataset for browsing and scenario selection.

### Local runtime

`web/local_server.py` serves the static frontend and routes `/api/predict` to the prediction handler.

## Input and output

The deployed model expects 42 numeric features. The API accepts a feature-name list and a list of rows. It returns predicted labels, confidence values, class probabilities, and class counts.

The API rejects missing features, invalid row shapes, non-numeric values, non-finite values, and requests exceeding 3,000 rows.

## Deployment boundary

The web application is an inference demonstration. It is not a continuous network packet sensor, an automated firewall, or a production alerting system.
