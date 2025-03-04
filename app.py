import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.title("Data Sweeper")
st.write("Upload your file and process it easily.")

uploaded_files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        st.write(f"File: {file.name}, Size: {file.size / 1024:.2f} KB")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning")
        remove_duplicates = st.checkbox(f"Remove duplicates from {file.name}")
        fill_missing_values = st.checkbox(f"Fill missing values in {file.name}")

        if remove_duplicates:
            df.drop_duplicates(inplace=True)
            st.success("Duplicates removed.")

        if fill_missing_values:
            numeric_cols = df.select_dtypes(include=["number"]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.success("Missing values filled.")

        # Select Columns for Conversion
        st.subheader("Select Columns to Convert")
        selected_columns = st.multiselect("Choose columns", df.columns, default=df.columns)

        if selected_columns:
            df = df[selected_columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        # File Conversion
        st.subheader("Convert File Format")
        conversion_type = st.radio("Convert file to:", ["CSV", "Excel"])

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
                new_file_name = file.name.replace(file_extension, ".csv")
            else:
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_file_name = file.name.replace(file_extension, ".xlsx")

            st.download_button("Download File", buffer.getvalue(), file_name=new_file_name, mime=mime_type)
