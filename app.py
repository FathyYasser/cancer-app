import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cancer Analysis Dashboard", layout="wide")

st.title("📊 Cancer Patients Analysis Dashboard")

# =====================
# Upload Data
# =====================
uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file, sep=';')
    df.columns = df.columns.str.strip()

    st.success("✅ Data Loaded Successfully!")

    # =====================
    # Preview
    # =====================
    st.subheader("📌 Data Preview")
    st.dataframe(df.head())

    # =====================
    # Basic Stats
    # =====================
    st.subheader("📊 Dataset Overview")
    st.write(df.describe(include='all'))

    # =====================
    # Filters Section
    # =====================
    st.sidebar.header("🔎 Filters")

    if "Gender" in df.columns:
        gender_filter = st.sidebar.multiselect("Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
        df = df[df["Gender"].isin(gender_filter)]

    if "Cancer_Type" in df.columns:
        type_filter = st.sidebar.multiselect("Cancer Type", df["Cancer_Type"].dropna().unique(), default=df["Cancer_Type"].dropna().unique())
        df = df[df["Cancer_Type"].isin(type_filter)]

    # =====================
    # Age Distribution
    # =====================
    if "Age" in df.columns:
        st.subheader("📈 Age Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["Age"].dropna(), bins=20)
        st.pyplot(fig)

    # =====================
    # Gender
    # =====================
    if "Gender" in df.columns:
        st.subheader("🚻 Gender Distribution")
        st.bar_chart(df["Gender"].value_counts())

    # =====================
    # Cancer Type
    # =====================
    if "Cancer_Type" in df.columns:
        st.subheader("🧬 Cancer Types")
        st.bar_chart(df["Cancer_Type"].value_counts())

    # =====================
    # Cancer Stage
    # =====================
    if "Cancer_Stage" in df.columns:
        st.subheader("⚕️ Cancer Stage Distribution")
        st.bar_chart(df["Cancer_Stage"].value_counts())

    # =====================
    # Smoking
    # =====================
    if "Smoking_Status" in df.columns:
        st.subheader("🚬 Smoking Status")
        st.bar_chart(df["Smoking_Status"].value_counts())

    # =====================
    # Outcome
    # =====================
    if "Outcome" in df.columns:
        st.subheader("🎯 Outcome Distribution")
        st.bar_chart(df["Outcome"].value_counts())

    # =====================
    # Hospital Analysis
    # =====================
    if "Hospital" in df.columns:
        st.subheader("🏥 Hospitals")
        st.bar_chart(df["Hospital"].value_counts())

    # =====================
    # Cause of Death
    # =====================
    if "Cause_of_Death" in df.columns:
        st.subheader("⚰️ Cause of Death")
        st.bar_chart(df["Cause_of_Death"].value_counts())

    # =====================
    # Correlation
    # =====================
    st.subheader("📊 Correlation (Numeric Features)")

    numeric_df = df.select_dtypes(include=['number'])

    if not numeric_df.empty:
        st.write(numeric_df.corr())
    else:
        st.write("No numeric data available for correlation.")