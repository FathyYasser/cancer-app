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
    if file.name.endswith(".csv"):
        return pd.read_csv(file, sep=None, engine="python")

    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file, engine="openpyxl")

# =========================
# TITLE
# =========================
st.title("🚀 Data Analysis Dashboard")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader(
    "📁 Upload File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        df.columns = df.columns.str.strip()
        st.session_state.df = df
        st.success("File uploaded successfully ✅")

    except Exception as e:
        st.error(f"Error reading file ❌\n{e}")

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

    filtered_df = df.copy()

    for col in cat_cols:
        unique_vals = filtered_df[col].dropna().unique()
        selected_vals = st.sidebar.multiselect(col, unique_vals)

        if selected_vals:
            filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

    # =========================
    # CLEANING
    # =========================
    st.subheader("🧹 Data Cleaning")

    c1, c2 = st.columns(2)

    if c1.button("Remove Null Values"):
        filtered_df = filtered_df.dropna()
        st.session_state.df = filtered_df

    if c2.button("Remove Duplicates"):
        filtered_df = filtered_df.drop_duplicates()
        st.session_state.df = filtered_df

    st.download_button(
        "⬇ Download Clean Data",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "clean_data.csv",
        "text/csv"
    )

    # =========================
    # OVERVIEW
    # =========================
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", filtered_df.shape[0])
    col2.metric("Columns", filtered_df.shape[1])
    col3.metric("Missing Values", filtered_df.isnull().sum().sum())

    # =========================
    # PREVIEW
    # =========================
    st.subheader("📌 Data Preview")
    st.dataframe(filtered_df.head(), use_container_width=True)

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

            data = filtered_df[col].value_counts().head(10)

            fig, ax = plt.subplots(figsize=(6, 4))

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

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(filtered_df[col].dropna().reset_index(drop=True))
            ax.set_title(col)

            st.pyplot(fig)

    # -------- HISTOGRAM --------
    elif chart_type == "Histogram":

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            col = st.selectbox("Select Numeric Column", num_cols)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(filtered_df[col].dropna(), bins=20)
            ax.set_title("Distribution")

            st.pyplot(fig)

    # -------- SCATTER --------
    elif chart_type == "Scatter Plot":

        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns")
        else:
            x = st.selectbox("X Axis", num_cols)
            y = st.selectbox("Y Axis", num_cols)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(filtered_df[x], filtered_df[y], alpha=0.5)

            ax.set_xlabel(x)
            ax.set_ylabel(y)

            st.pyplot(fig)

    # =========================
    # SMALL CORRELATION (OPTIONAL MINI VERSION)
    # =========================
    if len(num_cols) > 1:
        with st.expander("📉 Correlation Matrix (Optional)"):
            fig, ax = plt.subplots(figsize=(4, 3))

            sns.heatmap(
                filtered_df[num_cols].corr(),
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                linewidths=0.5,
                ax=ax
            )

            st.pyplot(fig)

else:
    st.info("📂 Please upload a CSV or Excel file to start")
