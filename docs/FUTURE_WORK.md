# Future Work and Research Roadmap

## 1. Stronger evaluation

- Repeat experiments across multiple random seeds.
- Use capture-file or device-based splits to reduce leakage from neighboring flows.
- Evaluate on an independently collected network dataset.
- Report confidence intervals and per-class uncertainty.

## 2. Feature reliability

- Investigate IAT, Number, and Weight individually.
- Verify feature definitions and availability in realistic network telemetry.
- Evaluate robustness when features are missing, noisy, or shifted.
- Document the exact feature extraction pipeline.

## 3. Rare attack categories

- Study class imbalance and rare-class recall.
- Evaluate class weighting and resampling approaches.
- Investigate precision-recall trade-offs and false-positive costs.
- Collect additional representative examples where permitted.

## 4. Explainability

- Extend SHAP analysis across attack categories.
- Study whether feature importance is stable across seeds and splits.
- Provide explanations that are understandable to security analysts.

## 5. Operational robustness

- Test inference latency and memory on constrained hardware.
- Add structured logging, monitoring, and model version tracking.
- Evaluate concept drift and retraining strategies.
- Test adversarial and out-of-distribution traffic.

## 6. Platform improvements

- Add authenticated analyst workspaces if required.
- Add alert review and feedback workflows.
- Add streaming ingestion only after a real packet/flow collection pipeline is designed and tested.
- Add model monitoring and dataset version tracking.

## Research boundary

These are proposed future improvements. They are not claimed as completed functionality in the current repository.
