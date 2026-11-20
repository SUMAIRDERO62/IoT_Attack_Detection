# IoT Cyber Threat Intelligence & Research Platform

An end-to-end machine learning research project for detecting and classifying IoT network attacks using the CIC-IoT2023 dataset.

The project covers dataset preparation, exploratory analysis, multi-class model evaluation, explainability research, model export, and an interactive web-based inference platform.

<p align="center">
   <a href="https://io-t-attack-detection.vercel.app/">Deployment</a> .
  <a href="https://github.com/SUMAIRDERO62/IoT_Attack_Detection">GitHub Repository</a> ·
  <a href="https://www.linkedin.com/in/sumair-ahmed-dero-70ba852a0">LinkedIn</a> ·
  <a href="https://sumair-ahmed-dero-ai-journey.vercel.app/">Portfolio</a>
</p>

---

## Project Overview

IoT environments contain diverse devices and network protocols, making them attractive targets for denial-of-service attacks, botnets, reconnaissance, brute-force attempts, spoofing, and web-based attacks.

This project investigates how supervised machine learning can identify benign and malicious network flows and classify attacks into broader categories.

The deployed inference artifact is an **8-class XGBoost model**. The web interface supports individual scenario inference, demo-flow exploration, and CSV batch prediction.

## Research Highlights

| Item | Details |
|---|---|
| Dataset | CIC-IoT2023 |
| Dataset source | Kaggle mirror documented below |
| Data sampling | 5% sample from each of 169 CSV files |
| Sampled rows | 2,334,322 |
| Rows after duplicate removal | 1,963,779 |
| Evaluation split | Stratified 80/20 split |
| Held-out test flows | 392,756 |
| Random seed | 42 |
| Compared models | Random Forest, XGBoost, LightGBM |
| Deployed model | XGBoost, 8 classes |
| Input features | 42 |
| Demo examples | 800 held-out test flows |

### Main evaluation results

Macro-F1 is emphasized because the dataset is highly imbalanced.

| Classification task | Random Forest | XGBoost | LightGBM |
|---|---:|---:|---:|
| Binary classification | 0.970 | 0.959 | 0.961 |
| 8 attack categories | 0.841 | 0.832 | 0.789 |
| 34 attack types | 0.809 | 0.828 | Not run |
| 8 classes without IAT, Number, Weight | 0.660 | 0.668 | 0.689 |

The deployed XGBoost model achieved **99.46% accuracy** on the full held-out 8-class test set, with a macro-F1 score of **0.832**.

The balanced 800-flow web demonstration achieved **86.5% accuracy (692/800)**. This is a separate evaluation subset and must not be confused with the full held-out test-set result.

Model export validation achieved 100% prediction agreement between the original and exported model on the 800 demonstration flows. Prediction agreement is not classification accuracy.

## Attack Categories

The web inference model predicts one of these eight categories:

1. Benign
2. BruteForce
3. DDoS
4. DoS
5. Mirai
6. Recon
7. Spoofing
8. Web

## Platform Features

- Interactive cybersecurity research dashboard.
- Live inference through the exported XGBoost model.
- Eight attack-category scenarios using real held-out demo examples.
- Inspection of all 42 model input features.
- Demo dataset browser with category filtering.
- CSV upload and batch inference.
- Input validation and prediction confidence.
- Class probability output.
- Downloadable prediction results.
- Research methodology, metrics, and limitations.
- Researcher profile, portfolio, and dataset attribution links.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| Data processing | Pandas, NumPy, PyArrow |
| Machine learning | Scikit-learn, XGBoost, LightGBM |
| Explainability | SHAP |
| Visualization | Matplotlib, Seaborn |
| Model serving | Python HTTP handler, XGBoost |
| Frontend | HTML, CSS, JavaScript |
| Deployment configuration | Vercel |
| Research environment | Kaggle Notebooks |

## Repository Structure

```text
IoT_Attack_Detection/
├── notebooks/
│   └── IoT_Attack_Detection_v2.ipynb
├── scripts/
│   └── export_web_files.py
├── figures/
├── results/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── METHODOLOGY.md
│   ├── RESULTS.md
│   ├── DEMO_GUIDE.md
│   └── FUTURE_WORK.md
├── web/
│   ├── api/
│   │   └── predict.py
│   ├── model/
│   │   ├── model_meta.json
│   │   └── xgb_8class.ubj
│   ├── public/
│   │   ├── index.html
│   │   ├── index-new.html
│   │   ├── demo_flows.json
│   │   └── figures/
│   ├── local_server.py
│   ├── requirements.txt
│   └── vercel.json
├── requirements.txt
├── LICENSE
└── README.md
```

## Run the Web Platform Locally

### 1. Clone the repository

```bash
git clone https://github.com/SUMAIRDERO62/IoT_Attack_Detection.git
cd IoT_Attack_Detection
```

### 2. Create a virtual environment

Linux / WSL:

```bash
python3 -m venv ~/.venvs/iot-attack-detection
source ~/.venvs/iot-attack-detection/bin/activate
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install web dependencies

```bash
pip install -r web/requirements.txt
```

### 4. Start the local inference server

```bash
cd web
python local_server.py
```

Open:

http://localhost:8000

The local server loads the exported model and serves the frontend and prediction API from the same origin.

Keep the model files in `web/model/`. The server requires the model artifact and metadata.

## Prediction API

### Model information

```http
GET /api/predict
```

Returns model name, XGBoost version, feature names, class labels, and maximum batch size.

### Batch inference

```http
POST /api/predict
Content-Type: application/json
```

Request structure:

```json
{
  "columns": ["feature_1", "feature_2"],
  "rows": [[1.2, 3.4]]
}
```

The example above illustrates the API shape only. Actual requests must contain all 42 required model features and their numeric values.

The API validates feature availability, row shape, numeric values, finite values, and batch size. It returns predicted classes, confidence, class probabilities, and prediction counts.

Maximum batch size: 3,000 rows.

## Reproduce the Research

The main experiment is documented in:

`notebooks/IoT_Attack_Detection_v2.ipynb`

The notebook was developed in Kaggle.

1. Open Kaggle Notebooks.
2. Import the repository notebook.
3. Add the CIC-IoT2023 dataset input.
4. Install or select compatible dependencies.
5. Run the notebook cells in order.
6. Review preprocessing, experiments, evaluation, and explainability outputs.

The notebook uses a 5% per-file sampling strategy and random seed 42. Full raw dataset files are not stored in this GitHub repository.

## Dataset and Attribution

**Kaggle dataset input used in the project:**

https://www.kaggle.com/datasets/madhavmalhotra/unb-cic-iot-dataset

**Official CIC-IoT2023 dataset page:**

https://www.unb.ca/cic/datasets/iotdataset-2023.html

**Research paper:**

Neto, E. C. P., Dadkhah, S., Ferreira, R., Zohourian, A., Lu, R., & Ghorbani, A. A. (2023). CICIoT2023: A real-time dataset and benchmark for large-scale attacks in IoT environment. *Sensors, 23*(13), 5941.

https://doi.org/10.3390/s23135941

The dataset is owned by its respective authors/institution and is subject to its own terms. Please cite the original dataset paper when using it.

## Research Limitations

- The experiments use a 5% sample rather than the complete dataset.
- Evaluation uses one stratified random split and one seed.
- Similar network flows from the same capture may appear across the split, potentially making the evaluation optimistic.
- Rare attack classes have limited test examples and less stable recall.
- Removing IAT, Number, and Weight reduces 8-class macro-F1 substantially, indicating dependence on these features.
- The real-world meaning and availability of all features should be verified before operational deployment.
- Performance on unseen networks, devices, and attack variants has not been established.
- The platform is a research demonstration, not a production network security appliance.

See `docs/RESULTS.md` and `docs/FUTURE_WORK.md` for more detail.

## Project Documentation

- [System Architecture](docs/ARCHITECTURE.md)
- [Research Methodology](docs/METHODOLOGY.md)
- [Experimental Results](docs/RESULTS.md)
- [Demonstration Guide](docs/DEMO_GUIDE.md)
- [Future Work](docs/FUTURE_WORK.md)
- [Web Application Guide](web/README.md)

## Author

**Sumair Ahmed**  
Department of Artificial Intelligence, University of Sindh

- LinkedIn: https://www.linkedin.com/in/sumair-ahmed-dero-70ba852a0
- Portfolio: https://sumair-ahmed-dero-ai-journey.vercel.app/
- GitHub: https://github.com/SUMAIRDERO62

## License

The source code is released under the MIT License. See [LICENSE](LICENSE).

The dataset remains subject to its original license and terms.
