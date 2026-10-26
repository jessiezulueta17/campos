"""
OPTIONAL model-training utility.

Use only if your instructor permits training a new model for this lab.
This is NOT a replacement for a required original midterm model.
Before running, verify the target column and input features with your instructor.
The default target is Usage_Status and leakage-prone/derived columns are excluded.
No results are pre-filled: metrics are computed from the actual uploaded CSV.
"""
from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

DATA_PATH = Path("facility_reservations.csv")
MODEL_DIR = Path("models")
TARGET = "Usage_Status"
EXCLUDE = {
    TARGET, "Reservation_Outcome", "Attendance_Ratio",
    "Submission_Date", "Reservation_Date"
}

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Place your real facility_reservations.csv in the project root first. "
            "Do not use a made-up dataset."
        )
    df = pd.read_csv(DATA_PATH)
    if TARGET not in df.columns:
        raise ValueError(f"Target '{TARGET}' was not found. Verify the correct target before training.")
    df = df.dropna(subset=[TARGET]).copy()
    y = df[TARGET].astype(str)
    X = df.drop(columns=[c for c in EXCLUDE if c in df.columns], errors="ignore")
    X = X.drop(columns=[c for c in X.columns if c.lower().endswith("_outcome")], errors="ignore")
    if X.empty:
        raise ValueError("No feature columns remain after excluding target/leakage columns.")
    if y.nunique() < 2:
        raise ValueError("The target has fewer than two classes; a classifier cannot be evaluated.")
    if len(df) < 10:
        raise ValueError("Too few labeled rows for a meaningful train/test split.")

    numeric_features = X.select_dtypes(include="number").columns.tolist()
    categorical_features = [c for c in X.columns if c not in numeric_features]
    transformers = []
    if numeric_features:
        transformers.append(("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median"))
        ]), numeric_features))
    if categorical_features:
        transformers.append(("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical_features))
    preprocess = ColumnTransformer(transformers=transformers)
    pipeline = Pipeline([
        ("preprocess", preprocess),
        ("classifier", RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"))
    ])

    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    metrics = {
        "target": TARGET,
        "test_rows": int(len(y_test)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision_weighted": float(precision_score(y_test, pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, pred, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, pred, average="weighted", zero_division=0)),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "features": list(X.columns),
        "warning": "Metrics are based on this dataset and split; review class balance, leakage, and suitability before use."
    }
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_DIR / "trained_model.joblib")
    (MODEL_DIR / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("Saved model to models/trained_model.joblib")
    print("Saved genuine evaluation metrics to models/model_metrics.json")
    print(json.dumps({k: v for k, v in metrics.items() if k != "classification_report"}, indent=2))

if __name__ == "__main__":
    main()
