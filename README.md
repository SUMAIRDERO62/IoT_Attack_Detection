# Scalable and Explainable Machine Learning for IoT Attack Detection

Attack detection on the **CIC-IoT-2023** dataset: data preparation, a comparison of three tree-based models
(Random Forest, LightGBM, XGBoost) on three tasks of increasing difficulty, an explanation of the best boosted model
with SHAP, and a small web demo.

**Live demo:** https://YOUR-PROJECT.vercel.app   *(replace after deploying, see [web/README.md](web/README.md))*

Author: Sumair Ahmed, Department of Artificial Intelligence, University of Sindh

---

## Summary

- **Data:** CIC-IoT-2023, 46.6 million labelled network flows from 105 IoT devices, 33 attacks in 7 categories.
  A random 5% of every one of the 169 CSV files was used: 2,334,322 rows, 1,963,779 after removing duplicates.
- **Tasks:** attack or benign (2 classes), attack category (8 classes), exact attack type (34 classes).
- **Main metric:** macro-F1. The classes are extremely imbalanced (largest to smallest label 5,821 to 1), so accuracy is
  above 0.99 for every model and says almost nothing.
- **Result:** Random Forest and XGBoost are practically tied on the 8-class task (macro-F1 0.841 and 0.832).
  XGBoost is better on rare attack types, the Random Forest is by far the fastest at prediction.
- **Main caveat:** all models rely strongly on three features (`IAT`, `Number`, `Weight`). Without them the 8-class
  macro-F1 falls to 0.66 to 0.69. I could not verify what `IAT` measures, so both scores are reported.

## Results

Macro-F1 on a held-out test set of 392,756 flows (80/20 stratified split, one split, seed 42).
In brackets: accuracy.

| Task | Random Forest | XGBoost | LightGBM |
|---|---|---|---|
| 2 classes | **0.970** (0.9967) | 0.959 (0.9952) | 0.961 (0.9955) |
| 8 classes | **0.841** (0.9945) | 0.832 (0.9946) | 0.789 (0.9939) |
| 34 classes | 0.809 (0.9919) | **0.828** (0.9918) | not run |
| 8 classes, without `IAT`, `Number`, `Weight` | 0.660 (0.8831) | 0.668 (0.8551) | **0.689** (0.8608) |
| 2 classes, without `IAT`, `Number`, `Weight` | 0.941 (0.9935) | 0.927 (0.9909) | 0.930 (0.9913) |

Speed on the 8-class task (whole test set, shared Kaggle CPU, times change a little between runs):

| Model | Training | Prediction of 392,756 flows | Saved model |
|---|---|---|---|
| Random Forest (50 trees) | about 80 to 95 s | about 1 s | 38 MB |
| XGBoost (150 rounds) | about 165 to 205 s | about 5 to 6 s | 3 MB |
| LightGBM (200 rounds) | about 145 to 160 s | about 19 to 27 s | not saved |

### Findings

1. **Accuracy hides the weak classes.** A model that always predicts the most common class scores 0.69 accuracy but
   only 0.10 macro-F1 on the 8-class task.
2. **Floods are easy, rare attacks are hard.** DDoS, DoS and Mirai labels have a recall of 0.96 or higher. Web attacks
   and BruteForce are recognised worst (8-class recall of the Random Forest: Web 0.33, BruteForce 0.43).
3. **The two kinds of mistake are not equal (2 classes).** The Random Forest flags about 560 of 10,987 benign test flows
   as attacks and misses about 725 attacks. XGBoost flags about 50 benign flows and misses about 1,830 attacks.
4. **The task difficulty matters.** Macro-F1 falls from about 0.96 to 0.97 (2 classes) to about 0.83 to 0.84 (8 classes).
   The loss sits in the rare labels, not in the floods.
5. **Explainability (SHAP on the XGBoost model).** `IAT` carries 28.8% of the total importance and `Number` 12.6%;
   together with `Weight` the three features carry 43.2%. `IAT` is among the three most important features of every
   category.

### Figures

All figures are produced by the notebook and stored in [`figures/`](figures/).

| | |
|---|---|
| ![Model comparison](figures/09_model_comparison_8class.png) | ![Recall per category](figures/10_recall_per_category.png) |
| Model comparison, 8 classes | Recall per category |
| ![Recall per label](figures/12_recall_per_label_34class.png) | ![SHAP](figures/15_shap_global_importance.png) |
| Recall of the 34 exact attack types | Feature importance (SHAP) |

## Repository

```
.
├── notebooks/IoT_Attack_Detection_v2.ipynb   complete analysis, every step explained, with outputs
├── figures/                                  all figures of the notebook (PNG)
├── results/results.csv                       every model run: macro-F1, accuracy, times
├── scripts/export_web_files.py               exports the model and demo flows for the web app
├── web/                                      the Vercel app (static page + Python API)
├── requirements.txt                          environment of the notebook
└── README.md
```

## Reproduce the analysis

The notebook was run on Kaggle (CPU). It takes about 40 minutes.

1. Create a Kaggle notebook and import `notebooks/IoT_Attack_Detection_v2.ipynb`.
2. Add the dataset **UNB CIC IOT 2023 Dataset** (`madhavmalhotra/unb-cic-iot-dataset`) as an input.
3. Run all cells. The first cell with `QUICK = True` runs a small dry run in a few minutes.
   `RUN_34CLASS` and `RUN_SPLIT_CHECK` switch the slowest parts on or off.

The random seed is 42 everywhere. Library versions are in [`requirements.txt`](requirements.txt).
The raw data is not stored in this repository.

## Run or deploy the web demo

See [web/README.md](web/README.md). The page lets you classify 800 real test flows or upload your own CSV with the
42 feature columns of the model.

## Limitations

- One random 80/20 split and one seed. Differences of about 0.01 between models are not reliable.
  Neighbouring rows of a capture are similar, so a random split is probably somewhat optimistic.
- Only a 5% sample of the data, and no hyperparameter tuning (first configurations only).
- The rare labels have only 12 to 60 test rows, so their recall values are noisy.
- It is unclear what `IAT`, `Number` and `Weight` represent, and the models depend strongly on them.
- Prediction times were measured on the whole test set with all cores of a shared machine. They are not the latency of one
  flow on an IoT device.
- No neural network was trained.

### Future work

A stricter split (for example by capture file); removing `IAT` alone to see which of the three features the result
depends on; several seeds and tuning; a small neural network for comparison; more of the 46.6 million rows;
latency and memory on a small device such as a Raspberry Pi.

## Dataset and citation

Neto, E. C. P., Dadkhah, S., Ferreira, R., Zohourian, A., Lu, R., Ghorbani, A. A. (2023).
*CICIoT2023: A real-time dataset and benchmark for large-scale attacks in IoT environment.*
Sensors, 23(13), 5941. https://doi.org/10.3390/s23135941

The dataset belongs to the Canadian Institute for Cybersecurity (University of New Brunswick) and must be cited when it
is used. Kaggle mirror used here: `madhavmalhotra/unb-cic-iot-dataset`.

## Licence

The code is released under the MIT licence (see [LICENSE](LICENSE)). The dataset has its own terms.
