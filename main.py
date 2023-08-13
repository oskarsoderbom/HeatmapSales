# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import os

# Adjust the layout of the Streamlit app
st.set_page_config(layout="centered")

# Inject custom CSS to enlarge the map display area
st.markdown(
    """
    <style>
        .folium-map {
            width: 150%;
            height: 600px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title for the Streamlit app
st.title('Sales Heatmap Dashboard')

# Add a file uploader to the Streamlit app
uploaded_file = st.file_uploader("Choose an Excel file (or leave empty to use the default)", type=["xlsx"])

# If no file is uploaded, use the default file
if uploaded_file is None:
    data = pd.read_excel("excel-sample (1).xlsx")
else:
    data = pd.read_excel(uploaded_file)

aggregated_sales = data.groupby('zip codes').agg({'Sales': 'sum'}).reset_index()

# Generate random latitude and longitude values for ZIP codes
aggregated_sales['Latitude'] = np.random.uniform(24.396308, 49.384358, size=len(aggregated_sales))
aggregated_sales['Longitude'] = np.random.uniform(-125.000000, -66.934570, size=len(aggregated_sales))

# Create the heatmap
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
heat_data = [[row['Latitude'], row['Longitude'], row['Sales']] for index, row in aggregated_sales.iterrows()]
HeatMap(heat_data).add_to(m)

# Display the folium map with streamlit_folium
folium_static(m)


map_file = "heatmap.html"
m.save(map_file)

# Provide a link to download the map
if os.path.exists(map_file):
    with open(map_file, "rb") as f:
        btn = st.download_button(
            label="Download Heatmap",
            data=f,
            file_name="heatmap.html",
            mime="text/html"
        )