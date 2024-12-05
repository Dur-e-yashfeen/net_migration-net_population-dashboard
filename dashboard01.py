import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import wbdata
from datetime import datetime

# Data Preparation
# Define countries: India (IND), Pakistan (PAK), Bangladesh (BGD), Afghanistan (AFG), Sri Lanka (LKA)
countries = ["IND", "PAK", "BGD", "AFG", "LKA"]

# Define indicators for Total Population and Net Migration
indicators = {
    'SP.POP.TOTL': 'Total Population',  # Total Population
    'SM.POP.NETM': 'Net Migration'      # Net Migration
}

# Define the date range
start_date = datetime(1960, 1, 1)
end_date = datetime(2023, 12, 31)

# Fetch data from the World Bank API
df = wbdata.get_dataframe(indicators, country=countries)

# Reset index and clean data
df = df.reset_index()  # Convert multi-index to columns
df['year'] = pd.to_datetime(df['date']).dt.year  # Extract year

# Filter data for the specified range
df = df[(df['year'] >= 1960) & (df['year'] <= 2023)]
df = df.dropna()  # Remove rows with missing data

# Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"])

# Layout Definition
app.layout = html.Div(
    id="dashboard-container", 
    children=[
        html.H1("SARR Country Population and Migration Dashboard by SciVue", className="text-center mt-4"),
        html.Div([
            html.Label("Select Countries:", className="form-label"),
            dcc.Dropdown(
                id="country-selector",
                options=[{"label": country, "value": country} for country in df["country"].unique()],
                value=["PAK"],  # Default value
                multi=True,
                className="mb-4"
            ),
            html.Label("Select Year Range:", className="form-label"),
            dcc.RangeSlider(
                id="year-slider",
                min=1960,
                max=2023,
                value=[1960, 2023],
                marks={year: str(year) for year in range(1960, 2024, 5)},
                className="mb-4"
            ),
            html.Label("Select Dashboard Background Color:", className="form-label"),
            dcc.Input(
                id="bg-color-picker",
                type="text",
                value="#FFFFFF",
                placeholder="Enter a color (e.g., #FFFFFF, lightblue)",
                className="mb-4"
            ),
        ], className="container"),
        html.Div([
            dcc.Graph(id="line-plot", className="mb-5"),
            dcc.Graph(id="line-plot1", className="mb-5"),
            dcc.Graph(id="scatter-plot")
        ])
    ]
)

# Callbacks to Update Graphs and Background Color
@app.callback(
    [Output("line-plot", "figure"),
     Output("line-plot1", "figure"),
     Output("scatter-plot", "figure"),
     Output("dashboard-container", "style")],
    [Input("country-selector", "value"),
     Input("year-slider", "value"),
     Input("bg-color-picker", "value")]
)
def update_graphs_and_style(selected_countries, selected_years, bg_color):
    filtered_df = df[(df["country"].isin(selected_countries)) & 
                     (df["year"] >= selected_years[0]) & 
                     (df["year"] <= selected_years[1])]

    # Line Plot for Total Population
    line_fig = px.line(
        filtered_df,
        x="year",
        y="Total Population",
        color="country",
        title="Total Population Over Time",
        labels={"year": "Year", "Total Population": "Total Population"},
        markers=True
    )

    # Line Plot for Net Migration
    line_fig1 = px.line(
        filtered_df,
        x="year",
        y="Net Migration",
        color="country",
        title="Net Migration Over Time",
        labels={"year": "Year", "Net Migration": "Net Migration"},
        markers=True
    )

    # Scatter Plot for Net Migration vs Total Population
    scatter_fig = px.scatter(
        filtered_df,
        x="Net Migration",
        y="Total Population",
        color="country",
        title="Net Migration vs Total Population",
        labels={"Net Migration": "Net Migration", "Total Population": "Total Population"},
        size="Total Population",
        hover_name="country"
    )

    # Update background color
    dashboard_style = {"backgroundColor": bg_color}

    return line_fig, line_fig1, scatter_fig, dashboard_style


# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)
