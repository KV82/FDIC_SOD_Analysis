import streamlit as st

st.set_page_config(
    page_title = "Home Page",
    page_icon = "👋",
)

st.write("# Welcome to the FDIC Summary of Deposits Analysis ! 👋")

st.sidebar.success("Select a dimension to analyze.")

st.markdown(
    """
    The FDIC publishes branch-level deposit data on an annual basis (Q2 data each year).
    
    **👈 Select a a dimension from the sidebar** to explore this further!
    #### Data sources: 
    - All data is publicly available from the FDIC website.
    - Check out [FDIC Summary of Deposits (SOD)](https://banks.data.fdic.gov/bankfind-suite/SOD/customDownload)
"""
)