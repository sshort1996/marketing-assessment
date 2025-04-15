import streamlit as st

def style_page():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #161C2E;
            color: #f0f0f0;
        }

        .stButton button {
            background-color: white;
            color: #DC2626;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.4rem 1rem;
            border: 1px solid #DC2626;
        }
        .stButton button:hover {
            background-color: #DC2626;
            color: white;
        }
        .stDownloadButton button {
            background-color: white;
            color: #DC2626; /* a nice red */
            font-weight: 600;
        }
        .stDownloadButton button:hover {
            background-color: #DC2626;
            color: white;
        }
        /* Style metric labels and values */
        .stMetric {
            background-color: white;
            color: #DC2626;
            border-radius: 6px;
            padding: 0.5rem;
            text-align: center;
            border: 1px solid #DC2626;
        }
        .stMetricLabel {
            font-weight: 600;
            color: #DC2626;
        }
        .stMetricValue {
            font-size: 1.2rem;
            font-weight: bold;
            color: #DC2626;
        }

        /* Style warning boxes */
        .stAlert {
            background-color: #DC2626;
            color: white;
            border-radius: 8px;
            padding: 0.75rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

