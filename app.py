import streamlit as st
import pandas as pd
from modules.data_processing import validate_dataset, clean_dataset, summarize_data_quality
from modules.exploratory_analysis import render_data_analysis
from modules.dashboard import render_dashboard
from modules.prediction import render_prediction_page
from modules.system_design import render_system_design

st.set_page_config(page_title="Facility Reservation Analytics", page_icon="📊", layout="wide")

st.title("Facility Reservation Analytics System")
st.caption("Systems Analysis and Design Laboratory • Streamlit deployment")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Dataset", "Data Analysis", "Prediction", "Dashboard", "System Design"]
)

st.sidebar.markdown("---")
st.sidebar.info("Upload your facility reservation CSV on the Dataset page. Model predictions remain unavailable until a real trained model is provided.")

if "raw_data" not in st.session_state:
    st.session_state.raw_data = None
if "clean_data" not in st.session_state:
    st.session_state.clean_data = None

if page == "Home":
    st.header("Home")
    st.write(
        "This application organizes the facility-reservation data workflow: upload and validate a dataset, "
        "review data quality, explore patterns, and view decision-support summaries."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Main workflow", "Upload → Clean")
    c2.metric("Analytics", "EDA + KPIs")
    c3.metric("Prediction status", "Model required")
    st.subheader("How to get started")
    st.markdown(
        "1. Open **Dataset** and upload your CSV file.\n"
        "2. Review the schema, missing values, and duplicate rows.\n"
        "3. Open **Data Analysis** and **Dashboard** to explore the actual data.\n"
        "4. Use **System Design** for the functional requirements and process flow.\n"
        "5. The **Prediction** page will load a saved model if one exists. It will not fabricate predictions or metrics."
    )
    st.warning("No model performance numbers are displayed unless a real saved model and evaluation report are available.")

elif page == "Dataset":
    st.header("Dataset Upload and Validation")
    upload = st.file_uploader("Upload facility reservation CSV", type=["csv"])
    if upload is not None:
        try:
            raw = pd.read_csv(upload)
            st.session_state.raw_data = raw
            valid, messages = validate_dataset(raw)
            st.session_state.clean_data = clean_dataset(raw)
            st.success(f"CSV loaded: {raw.shape[0]:,} rows × {raw.shape[1]:,} columns")
            for message in messages:
                (st.success if valid else st.warning)(message)
            st.subheader("Dataset preview")
            st.dataframe(raw.head(10), use_container_width=True)
            st.subheader("Data types")
            dtype_df = pd.DataFrame({"Column": raw.columns, "Data type": raw.dtypes.astype(str).values})
            st.dataframe(dtype_df, use_container_width=True)
            st.subheader("Data-quality summary")
            st.dataframe(summarize_data_quality(raw), use_container_width=True)
            st.download_button(
                "Download cleaned CSV",
                st.session_state.clean_data.to_csv(index=False).encode("utf-8"),
                file_name="facility_reservations_cleaned.csv",
                mime="text/csv"
            )
        except Exception as exc:
            st.error(f"Could not read this file as a CSV: {exc}")
    elif st.session_state.raw_data is not None:
        st.info("Previously uploaded data is available for this session.")
        st.dataframe(st.session_state.raw_data.head(10), use_container_width=True)
    else:
        st.info("Upload your CSV file to begin. The app does not assume or create a dataset for you.")

elif page == "Data Analysis":
    st.header("Exploratory Data Analysis")
    if st.session_state.clean_data is None:
        st.info("Upload a CSV file on the Dataset page first.")
    else:
        render_data_analysis(st.session_state.clean_data)

elif page == "Prediction":
    render_prediction_page()

elif page == "Dashboard":
    st.header("Decision-Support Dashboard")
    if st.session_state.clean_data is None:
        st.info("Upload a CSV file on the Dataset page first.")
    else:
        render_dashboard(st.session_state.clean_data)

elif page == "System Design":
    render_system_design()
