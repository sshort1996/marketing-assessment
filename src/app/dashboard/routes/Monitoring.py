import streamlit as st
from utils.mock_data import metadata

def generate_page():
    st.title("Logs & Monitoring")

    st.write("## Metadata Table")
    st.dataframe(metadata, height=300)

    # Quick stats with side-by-side metrics
    st.write("### Quick Stats")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Files", len(metadata))
    with col2:
        st.metric("Errors", metadata['status'].value_counts().get('error', 0))
    with col3:
        st.metric("Success", metadata['status'].value_counts().get('success', 0))

if __name__ == "__main__":
    generate_page()
