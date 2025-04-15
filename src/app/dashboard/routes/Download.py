import streamlit as st
import pandas as pd
from io import BytesIO
from utils.mock_data import data

def generate_page():
    st.title("Data Preview & Excel Download")

    # Limit preview data to max 100 rows
    preview_data = data.head(100)
    total_rows = len(preview_data)
    rows_per_page = 10

    # Track page number in session state
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    max_page = (total_rows - 1) // rows_per_page

    # Paginate data
    start_idx = st.session_state.page_num * rows_per_page
    end_idx = start_idx + rows_per_page
    page_data = preview_data.iloc[start_idx:end_idx]

    # Display table
    st.dataframe(page_data, height=300)


    # Pagination controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("←") and st.session_state.page_num > 0:
            st.session_state.page_num -= 1
    with col2:
        st.write(f"Page {st.session_state.page_num + 1} of {max_page + 1}")
    with col3:
        if st.button("→") and st.session_state.page_num < max_page:
            st.session_state.page_num += 1

    # Show message if truncated
    if len(data) > 100:
        st.warning("Data truncated to first 100 rows. Download to view the full dataset.")

    # Excel export function
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        return output.getvalue()

    excel_data = to_excel(data)

    # Download button
    st.download_button(
        label="Download Full Excel File",
        data=excel_data,
        file_name="sample_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    generate_page()
