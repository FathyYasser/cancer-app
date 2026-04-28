import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Data Dashboard",
    layout="wide",
    page_icon="📊"
)

# =========================
# SESSION STATE
# =========================
if "df" not in st.session_state:
    st.session_state.df = None

# =========================
# LOAD DATA (CSV + Excel)
# =========================
@st.cache_data
def load_data(file):
    try:
        # CSV
        if file.name.endswith(".csv"):
            return pd.read_csv(file, sep=None, engine='python')
        
        # Excel
        elif file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        
    except Exception as e:
        return None

# =========================
# TITLE
# =========================
st.title("🚀 Data Analysis Dashboard")

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📁 Upload File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    df = load_data(uploaded_file)

    if df is not None:
        df.columns = df.columns.str.strip()
        st.session_state.df = df
        st.success("File uploaded successfully ✅")
    else:
        st.error("Error reading file ❌")

# =========================
# GET DATA
# =========================
df = st.session_state.df

# =========================
# MAIN APP
# =========================
if df is not None:

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.header("⚙ Controls")

    chart_type = st.sidebar.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Pie Chart", "Line Chart", "Histogram", "Scatter Plot"]
    )

    # =========================
    # COLUMN TYPES
    # =========================
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = df.select_dtypes(include="number").columns.tolist()

    # =========================
    # FILTERS
    # =========================
    st.sidebar.subheader("🔍 Filters")

    for col in cat_cols:
        unique_vals = df[col].dropna().unique()
        selected_vals = st.sidebar.multiselect(col, unique_vals)

        if selected_vals:
            df = df[df[col].isin(selected_vals)]

    # =========================
    # CLEANING
    # =========================
    st
