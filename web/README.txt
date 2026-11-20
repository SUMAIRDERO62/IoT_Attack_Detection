# IoT Attack Detection — Model Bundle

This bundle contains the exported 8-class XGBoost model and demo data.

## Contents
- model/xgb_8class.ubj — exported XGBoost booster
- model/model_meta.json — 42 feature names and 8 class labels
- public/demo_flows.json — 800 demo rows, feature order, and ground-truth labels

## Model details
- Input features: 42
- Classes: Benign, BruteForce, DDoS, DoS, Mirai, Recon, Spoofing, Web
- Demo rows: 800

## Important
The model was exported from the Kaggle notebook and matched the original notebook model
on all 800 demo rows (100% prediction agreement). Demo accuracy reported by the notebook
was 86.5%.

Keep the model and metadata together. The feature order in model_meta.json must be
preserved when preparing prediction inputs.
