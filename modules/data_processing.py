import pandas as pd

EXPECTED_COLUMNS = [
    "Facility_Type", "User_Category", "Usage_Status",
    "Participants", "Actual_Attendance", "Lead_Time_Days",
    "Submission_Date", "Reservation_Date"
]

def validate_dataset(df):
    messages = []
    if df is None or df.empty:
        return False, ["The uploaded dataset is empty."]
    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        messages.append("Expected columns not found: " + ", ".join(missing))
        return False, messages
    messages.append("All expected reservation columns are present.")
    messages.append(f"Dataset contains {len(df):,} rows and {len(df.columns):,} columns.")
    return True, messages

def clean_dataset(df):
    """Return a cleaned copy; preserve the uploaded dataframe unchanged."""
    clean = df.copy()
    clean.columns = [str(c).strip() for c in clean.columns]
    for col in clean.select_dtypes(include=["object"]).columns:
        clean[col] = clean[col].map(lambda x: x.strip() if isinstance(x, str) else x)

    clean = clean.drop_duplicates().copy()

    for col in ["Participants", "Actual_Attendance", "Lead_Time_Days"]:
        if col in clean.columns:
            clean[col] = pd.to_numeric(clean[col], errors="coerce")
            clean.loc[clean[col] < 0, col] = pd.NA

    for col in ["Submission_Date", "Reservation_Date"]:
        if col in clean.columns:
            clean[col] = pd.to_datetime(clean[col], errors="coerce")

    if "Lead_Time_Days" in clean.columns and {"Submission_Date", "Reservation_Date"}.issubset(clean.columns):
        calculated = (clean["Reservation_Date"] - clean["Submission_Date"]).dt.days
        clean["Lead_Time_Days"] = clean["Lead_Time_Days"].fillna(calculated)
        clean.loc[clean["Lead_Time_Days"] < 0, "Lead_Time_Days"] = pd.NA

    if "Lead_Time_Days" in clean.columns:
        clean["Lead_Time_Category"] = pd.cut(
            clean["Lead_Time_Days"],
            bins=[-1, 7, 30, float("inf")],
            labels=["Short (0–7 days)", "Medium (8–30 days)", "Long (31+ days)"]
        )

    if "Usage_Status" in clean.columns:
        clean["Reservation_Outcome"] = clean["Usage_Status"].astype("string").str.strip().str.title()

    if {"Participants", "Actual_Attendance"}.issubset(clean.columns):
        denom = clean["Participants"].where(clean["Participants"] > 0)
        clean["Attendance_Ratio"] = clean["Actual_Attendance"] / denom

    return clean

def summarize_data_quality(df):
    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(x) for x in df.dtypes],
        "Missing Values": [int(df[c].isna().sum()) for c in df.columns],
        "Missing (%)": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        "Unique Values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })

def numeric_summary(df):
    numeric = df.select_dtypes(include="number")
    return numeric.describe().T if not numeric.empty else pd.DataFrame()
