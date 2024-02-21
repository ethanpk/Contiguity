!pip install folium

import streamlit as st
import folium
import json
import pandas as pd

# Load data
df = pd.read_csv("AlabamaUNS.csv")

# Read GeoJSON data containing Alabama zip code boundaries
alabama_geojson = 'alabamason.geojson'

# Filter GeoJSON features to include only those zip codes present in the data
filtered_features = []
with open(alabama_geojson, 'r') as f:
    geo_data = json.load(f)
    for feature in geo_data['features']:
        if feature['properties']['zip_code'] in df['ZIP Code'].values:
            filtered_features.append(feature)
    filtered_geo_data = {
        'type': 'FeatureCollection',
        'features': filtered_features
    }

# Create a Folium map
mymap = folium.Map(location=[32.8067, -86.7911], zoom_start=7)

# Add choropleth layer to the map
mymap.choropleth(
    geo_data=filtered_geo_data,
    data=df,
    columns=['ZIP Code', 'ZCTA UNS'],
    key_on='feature.properties.zip_code',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Scores by Zip Code'
)

# Add markers for each ZIP code with its score and population size
for index, row in df.iterrows():
    ZIP_code = row['ZIP Code']
    score = row['ZCTA UNS']
    PopulationSize = row['Population Size']

    try:
        location = [feature['geometry']['coordinates'][0][0][::-1] for feature in filtered_features if feature['properties']['zip_code'] == ZIP_code][0]
        folium.Marker(location=location, popup=f'Score: {score}<br>Population Size: {PopulationSize}').add_to(mymap)
    except:
        pass

# Convert Folium map to HTML
mymap_html = mymap._repr_html_()

# Display the map in Streamlit
st.markdown(mymap_html, unsafe_allow_html=True)
