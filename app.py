import streamlit as st
from utils import extract_page_with_part_number, extract_full_table_from_page
import pandas as pd
import io

st.set_page_config(page_title="Spare Parts Search", layout="wide")
st.title("🔍 Spare Parts Table Lookup")

# Upload the PDF
uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

# Search input
query = st.text_input("🔎 Enter part number (e.g., 93 872 600)")

# On search
if uploaded_file and query:
    with st.spinner("🔍 Searching..."):
        page_num, page = extract_page_with_part_number(uploaded_file, query)

        if page:
            df = extract_full_table_from_page(page)
            if not df.empty:
                st.success(f"✅ Found data on page {page_num + 1}")
                st.dataframe(df, use_container_width=True)

                # Export button
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                st.download_button("📥 Export to Excel", buffer, file_name="part_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("⚠️ Page found, but no table extracted.")
        else:
            st.error("❌ Part number not found.")
