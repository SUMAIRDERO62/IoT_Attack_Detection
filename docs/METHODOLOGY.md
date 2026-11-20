# Research Methodology

## Dataset

The experiments use CIC-IoT2023, a network-flow dataset developed for IoT attack research.

The Kaggle input documented by this project is:

https://www.kaggle.com/datasets/madhavmalhotra/unb-cic-iot-dataset

The original dataset page is:

https://www.unb.ca/cic/datasets/iotdataset-2023.html

A 5% sample was taken from each of 169 CSV files. The resulting sample contained 2,334,322 rows, reduced to 1,963,779 after duplicate removal.

## Tasks

Three classification tasks were investigated:

1. Binary classification: benign versus attack.
2. Eight-category classification: Benign, BruteForce, DDoS, DoS, Mirai, Recon, Spoofing, Web.
3. Thirty-four-class attack-type classification.

## Preprocessing and evaluation

The notebook documents preprocessing and feature preparation. The evaluation used a stratified 80/20 split and random seed 42. The held-out test set contained 392,756 flows.

The results are from one split and one seed. They should not be interpreted as proof of generalization to every network environment.

## Models

The research compared Random Forest, XGBoost, and LightGBM on the classification tasks.

The exported web model is the 8-class XGBoost model.

## Metrics

Macro-F1 is emphasized because class imbalance can make accuracy misleading. Accuracy, per-class recall, and other metrics are also considered in the research notebook.

## Explainability and feature dependence

The notebook includes SHAP-based analysis for the boosted model. An ablation experiment removing IAT, Number, and Weight reduced 8-class macro-F1 from 0.832 to 0.668 for XGBoost.

This indicates that the model relies materially on these features. Their availability and meaning should be verified in any target deployment environment.

## Reproducibility

The research notebook is the authoritative source for implementation details. It should be run with compatible package versions listed in the root `requirements.txt`. The raw dataset is not distributed in this repository.
