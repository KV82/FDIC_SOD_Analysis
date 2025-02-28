import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit import session_state as ss
import random

st.set_page_config(page_title = "Plotting Demo", page_icon = "📈")

st.markdown("# Branch Footprint")
st.sidebar.header("Branch locations")
st.write(
    """This plots branch locations for the North-East, Pennsylvania and the Upper Atlantic, organized into regions for easier analysis."""
)


# Reading the FDIC Summary of Deposits (SOD) data
df_branch_data = pd.read_csv('./FDIC/Data/SOD_CustomDownload_ALL_2024_06_30.csv')

# Reading the county-region mapping
df_county_cbr_mapping = pd.read_csv("./geospatial/data/CBR_County_Mapping.csv", dtype = str)

# Padding leading zero to get 5-character FIPS code
df_county_cbr_mapping['STCNTYBR'] = df_county_cbr_mapping['FIPS_Code'].str.pad(width = 5, side = 'left', fillchar = '0')

# Converting the FIPS code to a string to proceed with merging (aka lookup)
df_branch_data['STCNTYBR'] = df_branch_data['STCNTYBR'].astype(str)

df_branch_data = df_branch_data.merge(df_county_cbr_mapping, on = 'STCNTYBR', how = 'left')
df_branch_data.drop(['FIPS_Code', 'County', 'State'], axis = 1, inplace = True)

# Setting up the inter-dependent drop-down options
def on_banks_change():
    ss.region_options = df_branch_data[df_branch_data.NAMEFULL.isin(ss.banks)].CBR.unique()
    ss.county_options = df_branch_data[df_branch_data.NAMEFULL.isin(ss.banks) & df_branch_data.CBR.isin(ss.regions)].CNTYNAMB.unique()

def on_regions_change():
    ss.county_options = df_branch_data[df_branch_data.CBR.isin(ss.regions)].CNTYNAMB.unique()

if "bank_options" not in ss:
    ss.bank_options = df_branch_data.NAMEFULL.unique()
if "region_options" not in ss:
    ss.region_options = df_branch_data.CBR.unique()
if "county_options" not in ss:
    ss.county_options = df_branch_data.CNTYNAMB.unique()

col1, col2, col3 = st.columns(3)

col1.multiselect(
    label = "Select at least 1 bank",
    options = ss.bank_options,
    key = "banks",
    on_change = on_banks_change,
)

region_selection = col2.multiselect(
    label = "Select regions",
    options = ss.region_options,
    key = "regions",
    on_change = on_regions_change,
)

county_selection = col3.multiselect(
    label = "Select counties",
    options = ss.county_options,
    key = "counties",
    #on_change = on_counties_change,
)

# Filtering the dataframe based on the user selections
df_bank_filtered_branch_data = df_branch_data[df_branch_data['NAMEFULL'].isin(ss.banks) & df_branch_data['CBR'].isin(ss.regions) & df_branch_data['CNTYNAMB'].isin(ss.counties)]
st.write(
    "There are ", len(df_bank_filtered_branch_data) ," branches that meet the criteria selected above."
)

st.write('REMINDER #1  !!!! Place scrollable dataframe here, with data bars for visual aid for the marketshare / percentile.')

st.write('REMINDER #2  !!!! Use multiple layers - one for county boundary only + one for selected banks in color + one for all other banks in grey with greater opacity.')

st.write('REMINDER #3  !!!! Remove the bank as an option --- keep just the region and the county')

st.write('REMINDER #4  !!!! Add 2 tabs; one each for region mktshare and county mktshare')

st.write('REMINDER #5  !!!! Add slider to weed out the very smallest dots')

df_filtered_branch_data = df_branch_data[df_branch_data['CBR'].isin(ss.regions) & df_branch_data['CNTYNAMB'].isin(ss.counties)]

# Create the map
fig = px.scatter_mapbox(df_filtered_branch_data, 
                        lat = "SIMS_LATITUDE", 
                        lon = "SIMS_LONGITUDE", 
                        hover_name = "NAMEFULL", 
                        hover_data = ["NAMEBR"],
                        #mapbox_style = "open-street-map", 
                        mapbox_style = 'carto-positron',
                        color = "NAMEFULL",
                        zoom = 8,
                        opacity = 0.5,
                        size = "DEPSUMBR", 
                        size_max = 40
                        )

median_lat = df_filtered_branch_data['SIMS_LATITUDE'].median()
median_long = df_filtered_branch_data['SIMS_LONGITUDE'].median()
fig.update_layout(mapbox_center = {'lat': median_lat, 'lon': median_long + 0.075 }) # offset to handle the legend

fig.update_layout(
    legend = dict(
        x = 1,          # x-coordinate of the legend (0 is left, 1 is right)
        y = 1,          # y-coordinate of the legend (0 is bottom, 1 is top)
        xanchor = 'right', # Anchor point of x (can be 'left', 'center', 'right')
        yanchor = 'top'   # Anchor point of y (can be 'top', 'middle', 'bottom')
    )
)


# Display the map in Streamlit
st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
#st.button("Re-run")