import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(df):
    total = len(df)
    missing_cells = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows in current dataset", f"{total:,}")
    c2.metric("Missing cells", f"{missing_cells:,}")
    c3.metric("Duplicate rows", f"{duplicate_rows:,}")

    st.subheader("Reservation overview")
    if "Facility_Type" in df.columns:
        counts = df["Facility_Type"].fillna("Missing").astype(str).value_counts().rename_axis("Facility Type").reset_index(name="Reservations")
        st.plotly_chart(px.bar(counts, x="Facility Type", y="Reservations", title="Reservations by facility type"), use_container_width=True)
    if "Usage_Status" in df.columns:
        status = df["Usage_Status"].fillna("Missing").astype(str).value_counts().rename_axis("Usage Status").reset_index(name="Count")
        st.plotly_chart(px.bar(status, x="Usage Status", y="Count", title="Reservation status distribution"), use_container_width=True)
        st.caption("These are descriptive counts from the uploaded data, not model predictions.")

    st.subheader("Review queue")
    issues = []
    for idx, row in df.iterrows():
        reasons = []
        if row.isna().any():
            reasons.append("Missing field(s)")
        if "Participants" in df.columns and pd.notna(row.get("Participants")) and row.get("Participants") < 0:
            reasons.append("Negative participant count")
        if reasons:
            issues.append({"Row index": idx, "Review reason": "; ".join(reasons)})
    if issues:
        st.dataframe(pd.DataFrame(issues).head(100), use_container_width=True)
        st.caption("Review queue is based on data-quality flags only; it does not automatically approve or reject reservations.")
    else:
        st.success("No missing-field review flags found in the current dataset.")
