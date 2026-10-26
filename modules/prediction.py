from pathlib import Path
import json
import streamlit as st
import pandas as pd
import joblib

MODEL_PATH = Path("models/trained_model.joblib")
METRICS_PATH = Path("models/model_metrics.json")

def render_prediction_page():
    st.header("Prediction")
    st.write("This page only runs predictions from a genuine saved model pipeline.")
    if not MODEL_PATH.exists():
        st.warning("No trained model found at models/trained_model.joblib.")
        st.markdown(
            "The supplied notebook and Python script did not contain a saved model or visible training/evaluation code. "
            "No predictions or performance metrics are being invented."
        )
        st.markdown("**Next step:** locate the original midterm model, or ask your instructor whether training a new model is allowed. "
                    "If allowed, review `train_model.py` and run it only after confirming the correct target and features.")
        return

    try:
        model = joblib.load(MODEL_PATH)
    except Exception as exc:
        st.error(f"The saved model could not be loaded: {exc}")
        return

    if METRICS_PATH.exists():
        try:
            metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
            st.subheader("Saved evaluation metrics")
            st.json(metrics)
        except Exception:
            st.info("A metrics file exists but could not be read.")
    else:
        st.info("No saved evaluation metrics file was found. Do not interpret predictions as proof of model quality.")

    st.subheader("Predict from a CSV")
    st.caption("Upload a CSV containing the exact input columns expected by the saved pipeline.")
    uploaded = st.file_uploader("Upload prediction input CSV", type=["csv"], key="prediction_csv")
    if uploaded:
        try:
            inputs = pd.read_csv(uploaded)
            st.dataframe(inputs.head(), use_container_width=True)
            if st.button("Run prediction"):
                predictions = model.predict(inputs)
                output = inputs.copy()
                output["Model_Prediction"] = predictions
                st.dataframe(output, use_container_width=True)
                st.download_button("Download predictions", output.to_csv(index=False).encode("utf-8"),
                                   file_name="predictions.csv", mime="text/csv")
                st.caption("Use predictions as decision support only. A person should review relevant context before taking action.")
        except Exception as exc:
            st.error(f"Prediction failed. Check that the input columns match the saved pipeline. Details: {exc}")
