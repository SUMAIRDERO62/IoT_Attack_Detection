# Web demo (Vercel)

A static page (`public/index.html`) and one Python function (`api/predict.py`) that serves the
8-class XGBoost model.

```
web/
├── api/predict.py          GET: model information, POST: classify flows
├── public/index.html       the page
├── public/demo_flows.json  800 demo flows from the test set        (written by scripts/export_web_files.py)
├── public/figures/         PNG figures shown on the page           (copied from the notebook output)
├── model/xgb_8class.ubj    the XGBoost model                       (written by scripts/export_web_files.py)
├── model/model_meta.json   feature order and class names           (written by scripts/export_web_files.py)
├── requirements.txt        only what the API needs (numpy, scipy, xgboost-cpu)
├── vercel.json
└── .python-version
```

The API uses `xgboost-cpu`, the CPU-only build of XGBoost. It is a few MB instead of several hundred and is the
same version (3.4.1) that trained the model.

## Deploy
1. Push the repository to GitHub.
2. On vercel.com choose **Add New, Project** and import the repository.
3. Set **Root Directory** to `web`, **Framework Preset** to `Other` and leave the Build Command empty.
4. Click **Deploy**.

If the page shows 404, check that Root Directory is `web` and Output Directory is `public`.
If the page loads but says the API is not reachable, open the function logs in the Vercel dashboard and check that
`model/xgb_8class.ubj` and `model/model_meta.json` are in the repository.

## API
```
POST /api/predict
{"columns": ["flow_duration", ...], "rows": [[0.0, 54.0, ...], ...]}

200 {"predictions": ["DDoS", ...], "confidence": [0.99, ...], "probabilities": [[...], ...], "classes": [...], "summary": {...}}
400 {"error": "..."}
```
Columns can be in any order and extra columns are ignored. At most 3000 rows per request.
