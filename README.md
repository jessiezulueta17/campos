# Facility Reservation Analytics — Streamlit

A starter application for the Systems Analysis and Design lab. It reuses the existing facility-reservation cleaning/EDA workflow and adds the missing app structure.

## Important model note
The uploaded notebook and Python file were inspected and did not show model training, evaluation, prediction, or saving code. Therefore, this project does **not** include a fake trained model or invented performance numbers. The Prediction page explains that a model is missing until a real saved pipeline is added.

## Project structure
```text
facility_reservation_streamlit/
├── app.py
├── train_model.py                 # optional; only if instructor permits new training
├── requirements.txt
├── README.md
├── facility_reservations.csv       # add your real dataset here if training locally
├── modules/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── exploratory_analysis.py
│   ├── prediction.py
│   ├── dashboard.py
│   └── system_design.py
├── assets/
│   └── use_case_diagram.png
└── models/
    └── (place verified trained_model.joblib and model_metrics.json here)
```

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create/activate a virtual environment if desired.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start Streamlit:
   ```bash
   streamlit run app.py
   ```
6. Upload the real facility reservation CSV on the Dataset page.

## About optional training
Only run the training script if your instructor permits creating a new model rather than reusing the original midterm model. Verify the correct target and features first. The current script uses `Usage_Status` as a provisional target and excludes derived outcome/attendance fields to reduce leakage, but the target choice must be checked against the assignment and dataset meaning.

To use the optional training script, place your real dataset at `facility_reservations.csv` in the project root and run:
```bash
python train_model.py
```
The script trains and evaluates using a train/test split and saves the actual model and metrics. Do not report the metrics until you run it and inspect the output.

## Deploy to Streamlit Community Cloud
1. Put the project folder in a GitHub repository.
2. Include `requirements.txt`.
3. Add the real dataset only if your class/privacy rules allow it; otherwise upload the CSV in the running app.
4. In Streamlit Community Cloud, choose the repository and set the main file path to `app.py`.
5. Test all pages after deployment.

## Limitations
- Column names must match the expected schema for all features to be available.
- Predictions are decision-support only; they must not automatically approve or reject a reservation.
- The use case diagram and functional requirements are starter documentation and should be checked against your instructor's exact rubric.
