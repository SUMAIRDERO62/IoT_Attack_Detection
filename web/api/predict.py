"""Prediction API for the IoT attack detector (Vercel Python function).

GET  /api/predict  -> model information (feature names, class names)
POST /api/predict  -> {"columns": [...], "rows": [[...], ...]}
                      returns the predicted attack category and the class probabilities for every row
"""
import json
import os
from http.server import BaseHTTPRequestHandler

import numpy as np
import xgboost as xgb

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(os.path.dirname(HERE), "model")

MAX_ROWS = 3000          # keeps the request below Vercel's request size limit
MAX_BODY = 4_000_000     # bytes

# the model is loaded once per function instance, not once per request
with open(os.path.join(MODEL_DIR, "model_meta.json")) as f:
    META = json.load(f)
FEATURES = META["features"]
CLASSES = META["classes_8"]

BOOSTER = xgb.Booster()
BOOSTER.load_model(os.path.join(MODEL_DIR, "xgb_8class.ubj"))


def predict_rows(columns, rows):
    """Classify flows. `columns` names the columns of `rows`; they are put in the model's feature order."""
    if not isinstance(columns, list) or not isinstance(rows, list) or not rows:
        raise ValueError("send a list of column names and a non-empty list of rows")
    if len(rows) > MAX_ROWS:
        raise ValueError(f"at most {MAX_ROWS} rows per request (got {len(rows)})")

    index = {name: i for i, name in enumerate(columns)}
    missing = [name for name in FEATURES if name not in index]
    if missing:
        shown = ", ".join(missing[:8]) + (" ..." if len(missing) > 8 else "")
        raise ValueError(f"{len(missing)} required column(s) missing: {shown}")

    try:
        X = np.asarray(rows, dtype=np.float64)
    except (TypeError, ValueError):
        raise ValueError("every feature value must be a number")
    if X.ndim != 2 or X.shape[1] != len(columns):
        raise ValueError("every row must have one value per column")
    X = X[:, [index[name] for name in FEATURES]]
    if not np.isfinite(X).all():
        raise ValueError("values must be finite numbers (no empty cells, NaN or inf)")

    proba = BOOSTER.predict(xgb.DMatrix(X, feature_names=FEATURES))
    best = proba.argmax(axis=1)
    predictions = [CLASSES[i] for i in best]

    counts = {c: 0 for c in CLASSES}
    for p in predictions:
        counts[p] += 1

    return {
        "n_rows": int(X.shape[0]),
        "classes": CLASSES,
        "predictions": predictions,
        "confidence": [round(float(proba[i, b]), 4) for i, b in enumerate(best)],
        "probabilities": [[round(float(v), 4) for v in row] for row in proba],
        "summary": counts,
    }


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {
            "model": "XGBoost, 8 attack categories",
            "xgboost_version": xgb.__version__,
            "features": FEATURES,
            "classes": CLASSES,
            "max_rows": MAX_ROWS,
        })

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                return self._send(413, {"error": "request is too large"})
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = predict_rows(payload.get("columns"), payload.get("rows"))
            self._send(200, result)
        except json.JSONDecodeError:
            self._send(400, {"error": "the request body is not valid JSON"})
        except ValueError as err:
            self._send(400, {"error": str(err)})
        except Exception:
            self._send(500, {"error": "the model could not process this request"})

    def log_message(self, fmt, *args):
        pass
