import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_processing import numeric_summary

def render_data_analysis(df):
    st.subheader("Descriptive statistics")
    summary = numeric_summary(df)
    if summary.empty:
        st.write("No numeric columns are available for descriptive statistics.")
    else:
        st.dataframe(summary, use_container_width=True)

    chartable = [c for c in ["Facility_Type", "User_Category", "Usage_Status", "Lead_Time_Category", "Reservation_Outcome"] if c in df.columns]
    st.subheader("Interactive charts")
    if not chartable:
        st.info("No expected categorical fields were found. Check the uploaded CSV schema.")
        return

    c1, c2 = st.columns(2)
    with c1:
        col = st.selectbox("Chart 1: Count by category", chartable, key="eda_cat1")
        counts = df[col].fillna("Missing").astype(str).value_counts().rename_axis(col).reset_index(name="Count")
        st.plotly_chart(px.bar(counts, x=col, y="Count", title=f"Records by {col}"), use_container_width=True)
    with c2:
        col2 = st.selectbox("Chart 2: Distribution", chartable, index=min(1, len(chartable)-1), key="eda_cat2")
        counts2 = df[col2].fillna("Missing").astype(str).value_counts().rename_axis(col2).reset_index(name="Count")
        st.plotly_chart(px.pie(counts2, names=col2, values="Count", title=f"Distribution of {col2}"), use_container_width=True)

    st.markdown("**Chart 3: Numeric relationship**")
    numeric = list(df.select_dtypes(include="number").columns)
    if len(numeric) >= 2:
        x = st.selectbox("X-axis", numeric, key="eda_x")
        y = st.selectbox("Y-axis", [n for n in numeric if n != x], key="eda_y")
        st.plotly_chart(px.scatter(df, x=x, y=y, title=f"{y} compared with {x}"), use_container_width=True)
    elif numeric:
        selected = st.selectbox("Numeric column", numeric, key="eda_hist")
        st.plotly_chart(px.histogram(df, x=selected, title=f"Distribution of {selected}"), use_container_width=True)
    else:
        st.info("A numeric column is needed for the third chart.")
