# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
from datetime import datetime
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    coffee_shop = st.text_input("Which coffee shop do you visit most often?")
    favdrink = st.text_input("What is your favorite drink?")
    visit_time = st.text_input("When do you usually visit? (morning/afternoon/evening)")
    visits_per_week = st.number_input("How many times per week do you visit?", min_value=0, max_value=20, value=2)
    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        if coffee_shop.strip() and favdrink.strip() and visit_time.strip():
            new_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'coffee_shop': coffee_shop.strip(),
                'favdrink': favdrink.strip(),
                'visit_time': visit_time.strip(),
                'visits_per_week': visits_per_week
            }
            file_exists = os.path.exists('data.csv') and os.path.getsize('data.csv') > 0
            try:
                with open('data.csv', 'a', newline='') as csvfile:
                    fieldnames = ['timestamp', 'coffee_shop', 'favdrink', 'visit_time', 'visits_per_week']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(new_data)
                
                st.success("Your data has been submitted!")
                st.write(f"**Coffee Shop:** {coffee_shop}")
                st.write(f"**Favorite Drink:** {favdrink}")
                st.write(f"**Visit Time:** {visit_time}")
                st.write(f"**Visits/Week:** {visits_per_week}")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving data: {e}")
        else:
            st.error("❌ Please fill out all text fields before submitting.")

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    st.subheader("Data Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Entries", len(current_data_df))
    with col2:
        st.metric("Unique Coffee Shops", current_data_df['coffee_shop'].nunique())
    with col3:
        st.metric("Avg Visits/Week", f"{current_data_df['visits_per_week'].mean():.1f}")
    
    # Display the actual data
    st.subheader("Raw Data")
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
