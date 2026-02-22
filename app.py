import streamlit as st
import pandas as pd
from dealeron_scraper import run_dealeron_scraper
from staff_finder import run_staff_finder

st.title("Dealer Tools - Web Scraper")

option = st.radio("Choose Tool", ("DealerOn Vehicle Count Scraper", "Staff Finder"))

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    if option == "DealerOn Vehicle Count Scraper":
        st.write("Running DealerOn Scraper...")
        df = run_dealeron_scraper(uploaded_file)
    else:
        st.write("Running Staff Finder...")
        df = run_staff_finder(uploaded_file)

    if df is not None:
        st.success("Scraping complete!")
        st.dataframe(df)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv_data, "output.csv", "text/csv")
    else:
        st.error("Failed to scrape data.")
