"""Export the trained XGBoost model and a set of demo flows for the web app.

What it needs (all of them are written by the main notebook, section 16):
    xgb_8class.joblib, model_meta.json, demo_sample.csv

Where to run it
    Easiest: in a new Kaggle notebook that has the output of the main notebook attached as an input.
    Paste this whole file into one code cell and run it. Libraries must be the same versions as in
    the main notebook (xgboost 3.4.1, scikit-learn 1.6.1), because joblib files depend on them.
    Elsewhere:  python export_web_files.py --src <folder with the three files> --out web_export

What it writes (folder `web_export`, also zipped on Kaggle as web_export.zip):
    model/xgb_8class.ubj        the XGBoost booster in XGBoost's own binary format
    model/model_meta.json       feature order and class names
    public/demo_flows.json      800 demo flows from the test set (up to 100 per category)

Before it writes anything final it checks that the exported model gives the same predictions as the
original one on all demo flows.
"""
import argparse
import glob
import json
import os
import shutil

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder


class XGBLabelled:
    # the same wrapper class as in the main notebook; joblib needs it to load the saved model
    def __init__(self, **params):
        self.params = params
        self.enc = LabelEncoder()

    def fit(self, X, y):
        raise NotImplementedError("only used to load the saved model")

    def predict(self, X):
        return self.enc.inverse_transform(self.model.predict(X))


def find(name, src):
    folders = [src] if src else []
    folders += [".", "/kaggle/working", "/kaggle/input"]
    for folder in folders:
        hits = glob.glob(os.path.join(folder, "**", name), recursive=True)
        if hits:
            return hits[0]
    raise FileNotFoundError(f"{name} not found: attach the output of the main notebook or pass --src")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default=None, help="folder with the files written by the main notebook")
    parser.add_argument("--out", default=None, help="folder to write to (default: web_export)")
    args, _ = parser.parse_known_args()   # extra arguments (for example from a notebook) are ignored

    out = args.out or ("/kaggle/working/web_export" if os.path.isdir("/kaggle/working") else "web_export")
    os.makedirs(f"{out}/model", exist_ok=True)
    os.makedirs(f"{out}/public", exist_ok=True)

    # 1. load what the main notebook saved
    model = joblib.load(find("xgb_8class.joblib", args.src))
    meta = json.load(open(find("model_meta.json", args.src)))
    demo = pd.read_csv(find("demo_sample.csv", args.src))
    features = meta["features"]
    classes = meta["classes_8"]
    assert list(model.enc.classes_) == classes, "class order of the model and of model_meta.json differ"
    print("model loaded: %d features, %d classes, xgboost %s" % (len(features), len(classes), xgb.__version__))

    # 2. save the booster in XGBoost's own format and copy the meta file
    booster_path = f"{out}/model/xgb_8class.ubj"
    model.model.get_booster().save_model(booster_path)
    with open(f"{out}/model/model_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    # 3. demo flows: values written with 9 significant digits, which reproduces float32 exactly
    X = demo[features].to_numpy(dtype=np.float32)
    rows = [[float(f"{float(v):.9g}") for v in row] for row in X]
    true = demo["true_category"].tolist()

    # 4. check: the exported booster, fed with exactly what the web app will send, must agree
    #    with the original model on every demo flow
    web_booster = xgb.Booster()
    web_booster.load_model(booster_path)
    proba = web_booster.predict(xgb.DMatrix(np.array(rows, dtype=np.float64), feature_names=features))
    web_pred = [classes[i] for i in proba.argmax(axis=1)]
    original_pred = model.predict(demo[features]).tolist()
    agree = float(np.mean([a == b for a, b in zip(web_pred, original_pred)]))
    print("exported model agrees with the original on %.2f%% of the %d demo flows" % (agree * 100, len(rows)))
    assert agree == 1.0, "the exported model does not match the original: do not use these files"
    print("accuracy on the demo flows (up to 100 per category): %.3f"
          % np.mean([p == t for p, t in zip(web_pred, true)]))

    # 5. write the demo file
    with open(f"{out}/public/demo_flows.json", "w") as f:
        json.dump({"features": features, "classes": classes, "true": true, "rows": rows},
                  f, separators=(",", ":"))

    for path in sorted(glob.glob(f"{out}/**/*.*", recursive=True)):
        print(f"  {path}: {os.path.getsize(path) / 1e6:.2f} MB")

    if os.path.isdir("/kaggle/working"):
        archive = shutil.make_archive("/kaggle/working/web_export", "zip", out)
        print("zip for download:", archive)


if __name__ == "__main__":
    main()
