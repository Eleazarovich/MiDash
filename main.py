import pandas as pd
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go

df = pd.read_csv("newpop.csv")
df2 = pd.read_csv("monthly-precipitation.csv")
print(df2.head())

app = Dash()

y_axis = [i for i in range(1960, 2024)]
x_axis = [df[df["Country Name"] == "Sub-Saharan Africa"][str(i)].values[0] for i in y_axis]

dams_data = {
    "Dam": [
        "Grootdraai Dam", "Sterkfontein Dam", "Bloemhof Dam", 
        "Katse Dam", "Mohale Dam"
    ],
    "Current Week": [82.3, 98.2, 90.6, 70.5, 100.6],
    "Last Week": [83.2, 98.4, 91.1, 71.8, 100.6],
    "Last Year": [89.9, 99.6, 103.6, 92.5, 93.4]
}

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id="country-picker",
            options=[
                {'label': 'Africa Eastern and Southern', 'value': 'Africa Eastern and Southern'},
                {'label': 'Africa Western and Central', 'value': 'Africa Western and Central'},
                {'label': 'Botswana', 'value': 'Botswana'},
                {'label': 'Lesotho', 'value': 'Lesotho'},
                {'label': 'Sub-Saharan Africa', 'value': 'Sub-Saharan Africa'}
            ],
            value='Sub-Saharan Africa'
        )
    ], style={'width': '50%', 'margin': '0 auto'}),

    html.Div([
        dcc.Graph(
            id="sa-population",
        )
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id='dam-water-levels'
        )
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id="heat-map"
        )
    ], style={'width': '50%', 'display': 'inline-block'})
])

@app.callback(
    Output("sa-population", "figure"),
    [Input("country-picker", "value")]
)
def update_population_figure(selected_country):
    y_axis = [i for i in range(1960, 2024)]
    filtered_df = df[df["Country Name"] == selected_country]
    
    x_axis = [filtered_df[str(i)].values[0] for i in y_axis]

    trace = go.Scatter(
        x=y_axis,
        y=x_axis,
        mode="lines+markers",
        name="lines+markers"
    )

    return {
        "data": [trace],
        "layout": go.Layout(
            title=f"Population Growth in {selected_country}",
            xaxis={"title": "Year"},
            yaxis={"title": "Population"}
        )
    }

@app.callback(
    Output('dam-water-levels', 'figure'),
    [Input('dam-water-levels', 'id')]
)
def update_dam_levels_figure(_):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dams_data["Dam"],
        y=dams_data["Current Week"],
        name="Current Week",
        marker_color='rgb(26, 118, 255)'
    ))

    fig.add_trace(go.Bar(
        x=dams_data["Dam"],
        y=dams_data["Last Week"],
        name="Last Week",
        marker_color='rgb(55, 83, 109)'
    ))

    fig.add_trace(go.Bar(
        x=dams_data["Dam"],
        y=dams_data["Last Year"],
        name="Last Year",
        marker_color='rgb(50, 171, 96)'
    ))

    fig.update_layout(
        barmode='stack',
        title="Water Levels at Various Dams",
        xaxis_title="Dam",
        yaxis_title="Water Level (%)",
        legend_title="Time Period",
        template="plotly_white"
    )

    return fig

@app.callback(
    Output('heat-map', 'figure'),
    [Input('heat-map', 'id')])
def update_haat_map(_):
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        x=df2["Month"],
        y=df2["Year"],
        z=df2["PrecipitationJanuary"],
        colorscale="jet"
    ))

    fig.update_layout(
        title="Monthly Temprature",
        xaxis_title="Year",
        yaxis_title="Month")

    return fig

if __name__ == "__main__":
    app.run_server()