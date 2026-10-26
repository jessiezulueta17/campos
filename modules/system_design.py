from pathlib import Path
import streamlit as st

def render_system_design():
    st.header("System Design")
    st.subheader("Actors")
    st.markdown("- **System user / analyst:** uploads data, reviews validation results, explores charts, and reads dashboard summaries.\n"
                "- **Administrator / developer:** maintains the app, data schema, and any approved trained model.\n"
                "- **Reservation decision-maker:** reviews data flags and model output before deciding what action to take.")
    st.subheader("Functional requirements")
    requirements = [
        "The system shall accept a reservation dataset in CSV format.",
        "The system shall validate expected columns and show a preview.",
        "The system shall summarize missing values, duplicates, and data types.",
        "The system shall clean a copy of the uploaded data without overwriting the original upload.",
        "The system shall display descriptive statistics and at least three interactive charts when supported by the data.",
        "The system shall show dashboard KPIs and data-quality review flags.",
        "The system shall load a saved trained pipeline for predictions only when a valid model file exists.",
        "The system shall display evaluation metrics only when genuine saved metrics are available.",
        "The system shall not automatically approve or reject a reservation based on a model prediction."
    ]
    for item in requirements:
        st.markdown(f"- {item}")
    st.subheader("Analytical process flow")
    st.code("User uploads CSV\n  ↓\nValidate schema and preview data\n  ↓\nSummarize missing values and duplicates\n  ↓\nClean a copy of the data\n  ↓\nEDA charts and descriptive statistics\n  ↓\nDashboard KPIs and review flags\n  ↓\nIf a verified trained model exists: predict + display saved evaluation metrics\n  ↓\nHuman review and decision", language="text")
    diagram = Path("assets/use_case_diagram.png")
    if diagram.exists():
        st.subheader("Use case diagram")
        st.image(str(diagram), use_container_width=True)
    else:
        st.info("Use case diagram image not found; see the analytical process flow above.")
