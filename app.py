import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Data Analysis Dashboard",
    layout="wide",
    page_icon="📊"
)

# =========================
# SESSION STATE
# =========================
if "df" not in st.session_state:
    st.session_state.df = None

df = st.session_state.df

# =========================
# TITLE
# =========================
st.title("🚀 Data Analysis Dashboard")
st.write("Upload your dataset and explore it visually 📊")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.df.columns = st.session_state.df.columns.str.strip()
        df = st.session_state.df
        st.success("✅ File uploaded successfully!")
    except:
        st.error("❌ Error reading file")

# =========================
# MAIN APP
# =========================
if df is not None:

    # =========================
    # CLEANING
    # =========================
    st.subheader("🧹 Data Cleaning")

    c1, c2 = st.columns(2)

    if c1.button("Remove Null Values"):
        st.session_state.df = st.session_state.df.dropna()
        df = st.session_state.df
        st.success("Null values removed")

    if c2.button("Remove Duplicates"):
        st.session_state.df = st.session_state.df.drop_duplicates()
        df = st.session_state.df
        st.success("Duplicates removed")

    st.download_button(
        "⬇ Download Clean Data",
        df.to_csv(index=False).encode("utf-8"),
        "clean_data.csv",
        "text/csv"
    )

    # =========================
    # STATS
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

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Pie Chart", "Line Chart", "Histogram", "Scatter Plot"]
    )

    # =========================
    # COLUMNS FILTER (IMPORTANT FIX)
    # =========================
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    num_cols = df.select_dtypes(include="number").columns

    # =========================
    # BAR / PIE
    # =========================
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

    # =========================
    # LINE CHART
    # =========================
    elif chart_type == "Line Chart":

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            col = st.selectbox("Select Numeric Column", num_cols)
            st.line_chart(df[col].dropna())

    # =========================
    # HISTOGRAM
    # =========================
    elif chart_type == "Histogram":

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            col = st.selectbox("Select Column", num_cols)

            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20)
            ax.set_title("Distribution")
            st.pyplot(fig)

    # =========================
    # SCATTER PLOT
    # =========================
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
    # CORRELATION
    # =========================
    st.subheader("📉 Correlation Matrix")

    if len(num_cols) > 1:
        st.dataframe(df[num_cols].corr())
    else:
        st.info("Not enough numeric columns for correlation")

else:
    st.info("📂 Please upload a CSV file to start")
