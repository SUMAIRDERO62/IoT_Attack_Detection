# Web Application — IoT Threat Detection

This directory contains the exported 8-class XGBoost model, prediction API, local development server, and interactive dashboard.

## Components

- `api/predict.py` — model loading, input validation, and inference endpoint.
- `model/xgb_8class.ubj` — exported XGBoost model.
- `model/model_meta.json` — model feature names and class labels.
- `public/index.html` — primary dashboard.
- `public/index-new.html` — matching dashboard copy retained in the repository.
- `public/demo_flows.json` — 800 held-out demonstration flows.
- `local_server.py` — local server for the dashboard and API.
- `vercel.json` — Vercel function configuration.

## Requirements

Use Python 3.12 where possible.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r web/requirements.txt
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r web/requirements.txt
```

## Run locally

From the repository root:

```bash
cd web
python local_server.py
```

Open `http://localhost:8000`.

The terminal must remain open while using the dashboard. Stop the server with `Ctrl+C`.

## API contract

`GET /api/predict` returns model metadata.

`POST /api/predict` expects JSON with:

- `columns`: feature column names.
- `rows`: numeric feature rows.

The API requires all 42 model features. Column order may differ because the server reorders values into the model's expected feature order.

Maximum batch size is 3,000 rows. Non-numeric, missing, or non-finite values are rejected.

## Deploy to Vercel

1. Import this GitHub repository into Vercel.
2. Set the project root directory to `web`.
3. Use the Python runtime supported by the deployment platform.
4. Keep `vercel.json`, `api/`, `model/`, and `public/` in the configured project root.
5. Deploy and wait for the build to complete.
6. Test the deployed `/api/predict` endpoint with GET and POST requests.
7. Open the deployed homepage and test one scenario and one CSV batch.

Do not describe the application as publicly deployed until the deployment URL and API have been tested.

## Model and evaluation notes

The application serves the 8-class XGBoost artifact. The full held-out test-set accuracy was 99.46%, with macro-F1 0.832. The balanced 800-flow demonstration accuracy was 86.5%. These are separate evaluation results.

The 100% export agreement refers to prediction parity between the original and exported model on the demonstration flows, not classification accuracy.

## Troubleshooting

- `model loaded` confirms that the model and metadata were loaded by the local server.
- HTTP `000` from curl usually means the server is not running or the port is unreachable.
- If port 8000 is occupied, stop the other process or set another `PORT` before starting the server.
- If inference fails, verify that the model artifact, metadata, and web dependencies are present.
