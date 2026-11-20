# Experimental Results

## Evaluation setup

- Dataset: CIC-IoT2023.
- Sampling: 5% from each of 169 CSV files.
- Sample size before deduplication: 2,334,322.
- Sample size after deduplication: 1,963,779.
- Split: stratified 80/20.
- Held-out test flows: 392,756.
- Seed: 42.
- Primary metric: macro-F1.

## Macro-F1 comparison

| Task | Random Forest | XGBoost | LightGBM |
|---|---:|---:|---:|
| Binary | 0.970 | 0.959 | 0.961 |
| 8 categories | 0.841 | 0.832 | 0.789 |
| 34 attack types | 0.809 | 0.828 | Not run |
| 8 categories without IAT, Number, Weight | 0.660 | 0.668 | 0.689 |

## Deployed model

The web application serves the 8-class XGBoost model.

- Full held-out test accuracy: 99.46%.
- Full held-out test macro-F1: 0.832.
- Number of held-out test flows: 392,756.

## Demonstration subset

The web application contains 800 held-out test examples, balanced with up to 100 examples per category.

- Demo accuracy: 86.5%.
- Correct predictions: 692 of 800.
- Export parity: 100% prediction agreement between the original and exported model on the 800 demo examples.

Export parity means both model artifacts produced the same predictions. It does not mean every prediction was correct.

## Interpretation

Accuracy is high, but macro-F1 reveals weaker performance on less frequent classes. Random Forest achieved the highest 8-class macro-F1 in this experiment, while XGBoost was selected for the web inference artifact and achieved 0.832 macro-F1.

The experiment does not establish that XGBoost is universally superior. The results come from one random split and one seed.

## Feature ablation

Removing IAT, Number, and Weight reduced XGBoost 8-class macro-F1 from 0.832 to 0.668. This is an important limitation and a priority for follow-up research.

## Reproducibility note

The research notebook is the source of detailed metrics and outputs. No missing plots or confusion matrices are fabricated in this document.
