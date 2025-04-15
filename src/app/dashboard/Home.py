""" 
This is the Home page of our Streamlit application.

- Displays a short description of the data being presented.
- A row of pill icons at the top of the screen which can be 
  used to choose the current page.
- Sections separated by underlines, and a header with the 'Core' company logo.

The pages are accessed using streamlit fragments — when a pill button is clicked, 
the page logic is imported from 'pages/*' and run. Loading a single page does 
not force the full app to reload.
"""

import streamlit as st
from routes.Analytics import generate_page as generate_analytics_page
from routes.Download import generate_page as generate_download_page
from routes.Monitoring import generate_page as generate_monitoring_page
from Styling.styling import style_page

# Set page config — sidebar collapsed
st.set_page_config(
    page_title="Marketing Dashboard",
    initial_sidebar_state="collapsed"
)

style_page()
# --- App Header ---
st.image("assets/Core_Logo_White_CMYK.png", width=150)

def Home():
    st.title("Marketing Analytics Dashboard")
    st.write("""
             Welcome to the Core Marketing Analytics Dashboard — use the navigation tabs above to switch between views.\n
Available options:\n 
 - The analytics tab contains figures and tables for the processed data\n
 - The download tab contains a sample of the raw data, as well as an option to download the data in multiple file formats.\n
 - The monitoring tab contains summary statistics for the data pipeline, including logs, batch statistics, and any observed data quality issues.
             """)

st.markdown("---")

option_map = {
    0: r"$\color{red}{\textsf{Home}}$",
    1: r"$\color{red}{\textsf{Analytics}}$",
    2: r"$\color{red}{\textsf{ Excel Download}}$",
    3: r"$\color{red}{\textsf{Logging}}$",
}

selection = st.pills(
    "",
    options=option_map.keys(),
    default=0,
    format_func=lambda option: option_map[option],
    selection_mode="single",
)

st.markdown("---")

# --- Page Loader ---
if selection == 0:
    Home()

elif selection == 1:
    generate_analytics_page()

elif selection == 2:
    generate_download_page()

elif selection == 3:
    generate_monitoring_page()

