import streamlit as st

st.set_page_config(page_title="Media Dashboard", initial_sidebar_state="collapsed")

# --- Set up session state for selected page ---
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# Custom CSS for pill styling
st.markdown("""
<style>
.stButton > button {
    border-radius: 999px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    margin-right: 0.5rem;
    border: 2px solid transparent;
    background-color: white;
    color: #161C2E;
    transition: 0.3s;
}

/* Selected (active) state styling — using a custom class */
button.active-pill {
    background-color: #161C2E !important;
    color: white !important;
}

/* Borders per pill */
.stButton:nth-child(1) button { border-color: red; }
.stButton:nth-child(2) button { border-color: orange; }
.stButton:nth-child(3) button { border-color: #4ca3ff; }
.stButton:nth-child(4) button { border-color: violet; }
</style>
""", unsafe_allow_html=True)


# --- Pill Navigation ---
col1, col2, col3, col4 = st.columns(4)

def pill_button(label, key):
    # Check if this is the active page
    is_active = st.session_state.active_page == label

    # Apply active class dynamically
    button_class = "active-pill" if is_active else ""

    button_html = f"""
    <button class="{button_class}">{label}</button>
    """
    if st.markdown(button_html, unsafe_allow_html=True):
        st.session_state.active_page = label

# Render pill buttons inside columns
with col1:
    if st.button("🏠 Home"):
        st.session_state.active_page = "Home"
with col2:
    if st.button("📊 Analytics"):
        st.session_state.active_page = "Analytics"
with col3:
    if st.button("💾 Download"):
        st.session_state.active_page = "Download"
with col4:
    if st.button("📝 Logging"):
        st.session_state.active_page = "Logging"

# --- Show selected page ---
st.markdown("---")
st.write(f"**Selected Page:** {st.session_state.active_page}")
