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
# LOAD DATA (SMART)
# =========================
@st.cache_data
def load_data(file):
    try:
        return pd.read_csv(file, sep=None, engine='python')
    except:
        return None

# =========================
# TITLE
# =========================
st.title("🚀 Data Analysis Dashboard")

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

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
    # SIDEBAR (Controls)
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
    # FILTERS 🔥
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
    st.subheader("🧹 Data Cleaning")

    c1, c2 = st.columns(2)

    if c1.button("Remove Null Values"):
        df = df.dropna()
        st.session_state.df = df

    if c2.button("Remove Duplicates"):
        df = df.drop_duplicates()
        st.session_state.df = df

    st.download_button(
        "⬇ Download Clean Data",
        df.to_csv(index=False).encode("utf-8"),
        "clean_data.csv",
        "text/csv"
    )

    # =========================
    # OVERVIEW
    # =========================
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # =========================
    # PREVIEW
    # =========================
    st.subheader("📌 Data Preview")
    st.dataframe(df.head())

    # =========================
    # VISUALIZATION
    # =========================
    st.subheader("📈 Visualization")

    # -------- BAR / PIE --------
    if chart_type in ["Bar Chart", "Pie Chart"]:

        if len(cat_cols) == 0:
            st.warning("No categorical columns found")
        else:
            col = st.selectbox("Select Column", cat_cols)

            data = df[col].value_counts().head(10)

            fig, ax = plt.subplots()

            if chart_type == "Bar Chart":
                data.plot(kind="bar", ax=ax)
                plt.xticks(rotation=45)
            else:
                data.plot(kind="pie", autopct="%1.1f%%", ax=ax)

            st.pyplot(fig)

    # -------- LINE --------
    elif chart_type == "Line Chart":

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            col = st.selectbox("Select Numeric Column", num_cols)

            fig, ax = plt.subplots()
            ax.plot(df[col].dropna())
            ax.set_title(col)

            st.pyplot(fig)

    # -------- HISTOGRAM --------
    elif chart_type == "Histogram":

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            col = st.selectbox("Select Numeric Column", num_cols)

            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20)
            ax.set_title("Distribution")

            st.pyplot(fig)

    # -------- SCATTER --------
    elif chart_type == "Scatter Plot":

        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns")
        else:
            x = st.selectbox("X Axis", num_cols)
            y = st.selectbox("Y Axis", num_cols)

            fig, ax = plt.subplots()
            ax.scatter(df[x], df[y], alpha=0.5)

            ax.set_xlabel(x)
            ax.set_ylabel(y)

            st.pyplot(fig)

    # =========================
    # CORRELATION (Heatmap 🔥)
    # =========================
    st.subheader("📉 Correlation Matrix")

    if len(num_cols) > 1:
        fig, ax = plt.subplots()
        sns.heatmap(df[num_cols].corr(), annot=True, ax=ax)
        st.pyplot(fig)
    else:
        st.info("Not enough numeric columns")

else:
    st.info("📂 Please upload a CSV file to start")
