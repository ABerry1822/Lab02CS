# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.
import streamlit as st
import pandas as pd
import json
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Library and Coffee Study 📈")
st.write("Interact with library preferences and coffee habits")

# DATA LOADING
if 'graph_type' not in st.session_state:
    st.session_state.graph_type = 'bar'

st.divider()
st.header("Data Overview")

# Load CSV data
csv_data = None
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    try:
        csv_data = pd.read_csv('data.csv')
        st.success("✅ CSV data loaded successfully!")
        st.write(f"Survey entries: {len(csv_data)}")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
else:
    st.warning("No CSV data found. Submit some survey data first!")

# Load JSON data
json_data = None
if os.path.exists('data.json'):
    try:
        with open('data.json','r') as file:
            json_data = json.load(file)
        st.success("✅ JSON data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
else:
    st.error("JSON file not found!")

# GRAPH CREATION
st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH (Uses JSON data)
st.subheader("Graph 1: Library Study Spaces Comparison (Static Chart)")
if json_data:
    libraries = json_data['library_comparison']['libraries']
    lib_names = [lib['name'] for lib in libraries]
    study_seats = [lib['study_seats'] for lib in libraries]
    
    chart_data = pd.DataFrame({
        "Library": lib_names,
        'Study Seats': study_seats
    })
    
    # Using a different chart type - area chart
    st.area_chart(chart_data.set_index('Library')['Study Seats'])
    st.write("This **static area chart** compares the number of study seats available at different libraries from our JSON data.")

# GRAPH 2: DYNAMIC GRAPH (Uses JSON data)
st.subheader("Graph 2: Library Metrics Comparison (Dynamic Chart)")
if json_data:
    col1, col2 = st.columns(2)
    
    with col1:
        metric_choice = st.selectbox(
            "Choose metric to compare:",
            ["Hours Accessible", "Study Seat Availability", "WiFi Speed"])
    
    # Define data
    data = None
    metrics = json_data['library_comparison']['comparison_metrics']
    
    if metric_choice == "Hours Accessible":
        data = metrics['hours_accessible']
    elif metric_choice == "Study Seat Availability":
        data = metrics['study_seat_availability']
    else:  # WiFi Speed
        data = metrics['wifi_speed_mbps']
    
    with col2:
        sort_order = st.radio("Sort order:", ["Ascending", "Descending"])
    
    # Create and display chart
    if data is not None:
        chart_data = pd.DataFrame({
            'Library': list(data.keys()),
            'Value': list(data.values())
        })
        
        if sort_order == "Descending":
            chart_data = chart_data.sort_values('Value', ascending=False)
        
        # Using bar chart for this one
        st.bar_chart(chart_data.set_index('Library')['Value'])
        st.write(f"This **dynamic bar chart** shows {metric_choice} comparison between libraries. Users can select different metrics and sort order.")

# GRAPH 3: DYNAMIC GRAPH (Uses CSV data)
st.subheader("Graph 3: Coffee Shop Visit Patterns (Dynamic Chart)")
if csv_data is not None and not csv_data.empty:
    # Add interaction options
    col1, col2 = st.columns(2)
    
    with col1:
        chart_style = st.selectbox(
            "Choose chart style:",
            ["Average Visits", "Visit Distribution", "Time Pattern"]
        )
    
    with col2:
        if st.button("Switch Chart Type"):
            st.session_state.graph_type = "line" if st.session_state.graph_type == "bar" else "bar"
            st.rerun()  # This ensures immediate update
    
    # Create different visualizations based on selections
    if chart_style == "Average Visits":
        visits_by_shop = csv_data.groupby('coffee_shop')['visits_per_week'].mean()
        if st.session_state.graph_type == 'bar':
            st.bar_chart(visits_by_shop)
            st.write("**Dynamic bar chart** showing average weekly visits by coffee shop.")
        else:
            st.line_chart(visits_by_shop)
            st.write("**Dynamic line chart** showing average weekly visits by coffee shop.")
    
    elif chart_style == "Visit Distribution":
        # Scatter plot for distribution
        st.scatter_chart(csv_data, x='visits_per_week', y='coffee_shop')
        st.write("**Dynamic scatter chart** showing distribution of visits across coffee shops.")
    
    else:  # Time Pattern
        if 'timestamp' in csv_data.columns:
            try:
                time_data = csv_data.copy()
                time_data['timestamp'] = pd.to_datetime(time_data['timestamp'])
                time_data = time_data.sort_values('timestamp')
                time_series = time_data.groupby(time_data['timestamp'].dt.date)['visits_per_week'].sum()
                st.line_chart(time_series)
                st.write("**Dynamic line chart** showing visit patterns over time.")
            except:
                st.line_chart(csv_data.set_index('timestamp')['visits_per_week'])
                st.write("**Dynamic line chart** showing visit patterns over time.")
else:
    st.warning("No survey data available. Please submit data in the Survey page first.")
