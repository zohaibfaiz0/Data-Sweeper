import streamlit as st
import pandas as pd
import os
from io import BytesIO

# 🌟 Set Page Configuration (Light Mode)
st.set_page_config(page_title="💿 Data Sweeper", page_icon="📂", layout="wide")

# 🎨 Apply Custom Light Theme
st.markdown(
    """
    <style>
        /* Global Styling */
        body {background-color: #f8f9fa; color: #333;}
        .stApp {background-color: #ffffff;}

        /* Titles & Subheaders */
        h1, h2, h3 {color: #004aad !important; font-weight: bold;}

        /* File Uploader */
        .stFileUploader {border: 2px dashed #004aad !important; padding: 10px; background-color: #eef2ff !important;}

        /* DataFrame Styling */
        .stDataFrame {border-radius: 10px; overflow: hidden;}

        /* Buttons */
        .stButton>button {
            background-color: #004aad !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            border: none !important;
            font-size: 16px !important;
        }
        .stButton>button:hover {
            background-color: #003080 !important;
        }

        /* Download Button */
        .stDownloadButton>button {
            background-color: #009688 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-size: 16px !important;
        }
        .stDownloadButton>button:hover {
            background-color: #00796b !important;
        }

        /* Radio Buttons */
        .stRadio > div {flex-direction: row !important; gap: 10px !important;}

        /* Checkbox & Multiselect */
        .stMultiSelect, .stCheckbox {border-radius: 8px !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# 🎯 App Title & Description
st.title("💿 Data Sweeper")
st.markdown("🚀 **Transform your files between CSV and Excel formats** with built-in **data cleaning & visualization**.")

# 📂 File Upload Section
st.subheader("📤 Upload Your File(s)")
uploaded_file = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.markdown(f"📄 **File Name:** `{file.name}` | 📏 **File Size:** `{file.size / 1024:.2f} KB`")

        # 🔍 Data Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # 🛠️ Data Cleaning Section
        st.subheader("🛠️ Data Cleaning")
        if st.checkbox(f"🧹 Clean Data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed.")

            with col2:
                if st.button(f"📉 Fill Missing Values in `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled with mean.")

        # 🎛️ Column Selection
        st.subheader("🎛️ Select Columns to Keep")
        columns = st.multiselect("📌 Choose columns", df.columns, default=df.columns)
        df = df[columns]

        # 📊 Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Data Visualization for `{file.name}`"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        # 🔄 File Conversion
        st.subheader("🔄 File Conversion")
        convertion_types = st.radio(f"🔃 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📥 Convert `{file.name}`"):
            buffer = BytesIO()
            if convertion_types == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif convertion_types == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # ⬇️ Download Button
            st.download_button(
                label=f"⬇️ Download `{file_name}`",
                data=buffer,
                mime=mime_type,
                file_name=file_name
            )
            st.success("🎉 All Files Processed!")

# 🚀 Footer
st.markdown("---")
st.markdown("💡 **Tip:** Upload multiple files and process them one by one! 🚀")
