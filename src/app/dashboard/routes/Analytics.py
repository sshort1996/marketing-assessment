import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.mock_data import data

def generate_page():
    st.title("Analytics Dashboard")

    # Example Figure 1: distribution of a numeric column
    fig1 = px.histogram(data, x="value", nbins=20, title="Distribution of Values")
    st.plotly_chart(fig1)

    # Example Figure 2: time series trend
    fig2 = px.line(data, x="timestamp", y="value", title="Value over Time")
    st.plotly_chart(fig2)

    # Example Figure 3: category breakdown
    fig3 = px.bar(data.groupby("category").size().reset_index(name='counts'),
                  x="category", y="counts", title="Category Counts")
    st.plotly_chart(fig3)

if __name__ == "main":
    generate_page()
