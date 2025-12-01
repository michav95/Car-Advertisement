import pandas as pd
import streamlit as st
import plotly.express as px

# Load and prep the data
data = pd.read_csv("vehicles.csv")  # <- change to your actual filename

# Make sure numeric columns are numeric
numeric_cols = ['price', 'model_year', 'odometer', 'days_listed']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop rows with missing key numeric values
data = data.dropna(subset=['price', 'model_year', 'odometer', 'days_listed'])

# Create a helper column: age of vehicle
current_year = 2025  # or datetime.now().year
data['vehicle_age'] = current_year - data['model_year']

# Streamlit App
st.header('Used Vehicle Listings Analysis')

# Top 20 most common car models
model_counts = data['model'].value_counts().reset_index()
model_counts.columns = ['model', 'count']
top_models = model_counts.head(20)

show_top_models = st.checkbox('Show only Top 20 Models')
if show_top_models:
    data_models_filtered = data[data['model'].isin(top_models['model'])]
    st.write("Top Models:", top_models['model'].tolist())
else:
    data_models_filtered = data.copy()

fig_models_hist = px.histogram(
    top_models,
    x='model',
    y='count',
    labels={'model': 'Model', 'count': 'Number of Listings'},
    title='Top 20 Most Common Vehicle Models'
)
fig_models_hist.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_models_hist)

fig_models_scatter = px.scatter(
    top_models,
    x='model',
    y='count',
    labels={'model': 'Model', 'count': 'Number of Listings'},
    title='Frequency of Vehicle Models'
)
fig_models_scatter.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_models_scatter)

# Top 20 fastest-selling vehicles (lowest days_listed)
data_speed = data[data['days_listed'] > 0].copy()

# Sort by days_listed ascending (fastest first) and drop duplicates by model+year
fast_vehicles = (
    data_speed
    .sort_values(by=['days_listed', 'model', 'model_year', 'price', 'odometer'])
    .drop_duplicates(subset=['model', 'model_year'])
)

top_20_fast = fast_vehicles.head(20)

show_top_20_fast = st.checkbox('Show only Fast-Selling Vehicles')
if show_top_20_fast:
    data_fast_filtered = data[data['model'].isin(top_20_fast['model'])]
    st.write("Fast-Selling Vehicles (by model):", top_20_fast['model'].tolist())
else:
    data_fast_filtered = data.copy()

# Histogram of days listed for the top 20 fastest-selling vehicles
fig_fast_hist = px.histogram(
    top_20_fast,
    x='model',
    y='days_listed',
    labels={'model': 'Model', 'days_listed': 'Days Listed'},
    title='Top 20 Fastest-Selling Vehicle Models'
)
fig_fast_hist.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_fast_hist)

# Scatter for the same
fig_fast_scatter = px.scatter(
    top_20_fast,
    x='model',
    y='days_listed',
    labels={'model': 'Model', 'days_listed': 'Days Listed'},
    title='Days Listed for Fast-Selling Vehicle Models'
)
fig_fast_scatter.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_fast_scatter)

# Average days listed by vehicle type
type_speed = (
    data.groupby('type')['days_listed']
    .mean()
    .reset_index()
    .rename(columns={'days_listed': 'average_days_listed'})
)

fig_type_hist = px.histogram(
    type_speed,
    x='type',
    y='average_days_listed',
    labels={'type': 'Vehicle Type', 'average_days_listed': 'Average Days Listed'},
    title='Average Days Listed by Vehicle Type'
)
fig_type_hist.update_layout(xaxis_tickangle=-45)

fig_type_scatter = px.scatter(
    type_speed,
    x='type',
    y='average_days_listed',
    labels={'type': 'Vehicle Type', 'average_days_listed': 'Average Days Listed'},
    title='Average Days Listed by Vehicle Type (Scatter)'
)
fig_type_scatter.update_layout(xaxis_tickangle=-45)

# Selector to choose which chart to show
options = [
    'Average Days Listed by Type (Histogram)',
    'Average Days Listed by Type (Scatter)',
    'Fast-Selling Models (Histogram)',
    'Fast-Selling Models (Scatter)',
    'Top Models (Histogram)',
    'Top Models (Scatter)'
]

selected_option = st.selectbox('Choose a visualization:', options)

if selected_option == 'Average Days Listed by Type (Histogram)':
    st.plotly_chart(fig_type_hist)
elif selected_option == 'Average Days Listed by Type (Scatter)':
    st.plotly_chart(fig_type_scatter)
elif selected_option == 'Fast-Selling Models (Histogram)':
    st.plotly_chart(fig_fast_hist)
elif selected_option == 'Fast-Selling Models (Scatter)':
    st.plotly_chart(fig_fast_scatter)
elif selected_option == 'Top Models (Histogram)':
    st.plotly_chart(fig_models_hist)
elif selected_option == 'Top Models (Scatter)':
    st.plotly_chart(fig_models_scatter)

st.write(f"You selected: {selected_option}")
