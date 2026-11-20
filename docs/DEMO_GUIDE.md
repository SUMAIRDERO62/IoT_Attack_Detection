# Demonstration Guide

## Before the demonstration

1. Clone or open the repository.
2. Activate the Python environment.
3. Install `web/requirements.txt`.
4. Confirm that `web/model/model_meta.json` and `web/model/xgb_8class.ubj` exist.
5. Start the local server.

```bash
cd web
python local_server.py
```

Open `http://localhost:8000`.

## Suggested presentation flow

### 1. Introduce the research problem

Explain that IoT network traffic can contain benign activity and multiple attack categories. The project studies supervised ML classification on CIC-IoT2023.

### 2. Explain the dataset

Show the dataset source, sampling strategy, preprocessing, and class imbalance. Mention that the project uses a 5% sample from each of 169 CSV files.

### 3. Explain the experiments

Introduce Random Forest, XGBoost, and LightGBM. Explain why macro-F1 is more informative than accuracy for imbalanced labels.

### 4. Demonstrate live inference

Select a scenario from the eight categories and run the model prediction. Explain:

- Predicted class.
- Model confidence.
- Class probabilities.
- Ground-truth label for the selected held-out example.
- Input feature inspection.

A prediction can be wrong; the interface should display that honestly.

### 5. Explore demo flows

Use the sample browser to filter and inspect examples. These are held-out demonstration flows, not a live network feed.

### 6. Demonstrate CSV batch inference

Use a CSV with the exact 42 feature columns. The application validates numeric values and sends the rows to the inference API.

The maximum API batch size is 3,000 rows.

### 7. Discuss research findings and limitations

Present the 99.46% full held-out test accuracy separately from the 86.5% balanced demo accuracy. Explain the macro-F1 score of 0.832 and the feature-ablation result.

### 8. Conclude with future work

Discuss capture-based splits, external validation, rare-class performance, feature reliability, and deployment monitoring.

## Important presentation statements

- The application performs inference using an exported XGBoost model.
- The 800 demo examples come from held-out test data.
- Export agreement is not classification accuracy.
- The current interface is a research demonstration, not a production intrusion prevention system.
- Do not claim real-time packet capture or live network monitoring.
