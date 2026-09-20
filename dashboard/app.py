from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "master_table_tainan_2024_v2.csv"
PT_FIG_PATH = BASE_DIR / "docs" / "pt_per_10000_by_district.png"
SCATTER_FIG_PATH = (
    BASE_DIR / "docs" / "older_population_vs_pt_availability.png"
)
FACILITY_FIG_PATH = (
    BASE_DIR / "docs" / "rehab_medical_facility_per_10000_by_district.png"
)


st.set_page_config(
    page_title="Tainan Rehabilitation Accessibility",
    layout="wide"
)

#改顏色
st.markdown(
    """
    <style>

    /* Whole page */
    .stApp {
        background-color: #F6F8FB;
        color: #243447;
    }

    /* Main page width / spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Main title */
    h1 {
        color: #243447;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Section headings */
    h2, h3 {
        color: #3F7C85;
        font-weight: 650;
    }

    /* Normal text */
    p, li {
        color: #485563;
        line-height: 1.6;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #DDE5EB;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(36, 52, 71, 0.06);
    }

    /* KPI labels */
    [data-testid="stMetricLabel"] {
        color: #5F6B76;
        font-weight: 600;
    }

    /* KPI values */
    [data-testid="stMetricValue"] {
        color: #243447;
    }

    /* Captions */
    .stCaption {
        color: #71808F;
    }

    /* Dataframe container */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.title("Rehabilitation Service Accessibility")
st.subheader("Resource Gap Analysis: A Tainan Case Study")

st.write(
    """
    An exploratory district-level analysis of rehabilitation workforce,
    medical facility availability, and population demand in Tainan City, 2024.
    """
)


df = pd.read_csv(DATA_PATH)

# Summary indicators
total_pt = int(df["pt_count"].sum())

zero_pt_districts = int(
    (df["pt_count"] == 0).sum()
)

total_rehab_medical_facilities = int(
    df["rehab_medical_facility_count"].sum()
)

st.markdown("### Key Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Registered PTs",
    f"{total_pt:,}"
)

col2.metric(
    "Districts with 0 Registered PTs",
    zero_pt_districts
)

col3.metric(
    "Rehab Medical Facilities*",
    total_rehab_medical_facilities
)

st.caption(
    "*Includes rehabilitation hospitals and clinics only; "
    "physical therapy clinics are not included due to data availability limitations."
)

#第一張圖
st.markdown("### Physical Therapist Availability")

st.write(
    """
    PT availability is standardized by district population
    to allow comparison across districts with different population sizes.
    """
)

st.image(
    PT_FIG_PATH,
    use_container_width=True
)

#第二張圖
st.markdown("### Older Population Share vs PT Availability")

median_age = df["pct_65_plus"].median()
median_pt = df["pt_per_10000"].median()

priority_group = df[
    (df["pct_65_plus"] >= median_age)
    &
    (df["pt_per_10000"] <= median_pt)
].copy()

left_col, right_col = st.columns([2, 1])
with left_col:
    st.image(
        SCATTER_FIG_PATH,
        use_container_width=True
    )

with right_col:
    st.markdown("**Exploratory high-age / low-PT group**")

    priority_display = priority_group[
        [
            "district",
            "pct_65_plus",
            "pt_per_10000"
        ]
    ].sort_values(
        ["pct_65_plus", "pt_per_10000"],
        ascending=[False, True]
    )

    priority_display = priority_display.round(2)

    st.dataframe(
        priority_display,
        hide_index=True,
        use_container_width=True
    )

st.caption(
    "District medians are used only for exploratory comparison. "
    "This grouping does not represent an official threshold for "
    "rehabilitation resource shortage."
)

#第三張圖
st.markdown("### Rehabilitation Medical Facility Availability")

st.write(
    """
    Medical facility availability is measured using rehabilitation
    hospitals and rehabilitation clinics per 10,000 population.
    """
)

st.image(
    FACILITY_FIG_PATH,
    use_container_width=True
)

st.markdown("### Data Limitations")

st.markdown(
    """
    - **Physical therapy clinics are not included in the facility-level analysis.**
      A consistent 2024 district-level historical dataset could not be confirmed.
      Because physical therapy clinics are an important source of rehabilitation
      services, facility availability may therefore be underestimated in some districts.

    - **PT headcount does not equal actual service capacity.**
      Differences in working hours, treatment duration, service models,
      and patient volume are not captured in the available workforce data.

    - **Population aged 65+ is used as a proxy for potential rehabilitation demand.**
      A higher older-population share does not imply that all older residents
      require rehabilitation services.

    - The analysis describes **district-level resource distribution and potential gaps**,
      rather than proving actual unmet rehabilitation demand or individual accessibility.
    """
)

#District-level Summary Table + Research Question/Methods 說明
st.markdown("### Study Overview")

st.markdown(
    """
    **Research question:**  
    How are rehabilitation-related workforce and medical facilities distributed
    across the 37 districts of Tainan City, and where might relative resource gaps exist?

    **Unit of analysis:** 37 administrative districts in Tainan City

    **Reference year:** 2024

    **Demand-side indicators:** total population, population aged 65+, and proportion aged 65+

    **Supply-side indicators:** registered physical therapists, rehabilitation clinics,
    and hospitals with rehabilitation departments

    **Standardized indicators:** PTs per 10,000 population and rehabilitation medical
    facilities per 10,000 population
    """
)

st.markdown("### District-level Summary")

summary_table = df[
    [
        "district",
        "total_population",
        "population_65_plus",
        "pct_65_plus",
        "pt_count",
        "pt_per_10000",
        "rehab_medical_facility_count",
        "rehab_medical_facility_per_10000"
    ]
].copy()

summary_table = summary_table.round(2)

st.dataframe(
    summary_table,
    hide_index=True,
    use_container_width=True
)

st.caption(
    "Prototype dashboard developed as an independent graduate application project."
)