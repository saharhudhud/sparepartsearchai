import streamlit as st
from utils import extract_page_with_part_number, extract_structured_table_from_blocks

st.set_page_config(page_title="Part Number Table Search", layout="wide")
st.title("🔍 Spare Parts Search")

uploaded_file = st.file_uploader("Upload PDF Catalog", type="pdf")
query = st.text_input("Enter part number (e.g. 93 872 600)")

if uploaded_file and query:
    with st.spinner("Searching for part number and extracting table..."):
        page_num, blocks = extract_page_with_part_number(uploaded_file, query)
        
        if blocks:
            df = extract_structured_table_from_blocks(blocks)
            if not df.empty:
                st.success(f"✅ Table found on page {page_num + 1}")
                st.dataframe(df)

                if st.button("📥 Export to Excel"):
                    df.to_excel("matched_table.xlsx", index=False)
                    st.success("Exported to matched_table.xlsx")
            else:
                st.warning("Found the page, but couldn't extract the expected table.")
        else:
            st.error("Part number not found in PDF.")
