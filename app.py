# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime as dt

# Load Data
toronto_df = pd.read_csv('toronto_data.csv')
toronto_df['episode_date'] = pd.to_datetime(toronto_df['episode_date'])
# Array to hold age_group in order
age_order = ['19 and younger', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']


# Toronto Fig by Age
fig_age = px.histogram(toronto_df, x="age_group", y="outcome", histfunc="count")
fig_age.update_layout(xaxis={'categoryorder':'category ascending'})

# Toronto Fig by Gender
fig_gender = px.histogram(toronto_df, x="gender", y="outcome", histfunc="count")
fig_gender.update_layout(xaxis={'categoryorder':'category ascending'})

# Toronto Fig by Age
fig_age_outcome = px.histogram(toronto_df, x="outcome", y="age_group", histfunc="count", color='outcome', barmode='group', orientation='h')
fig_age_outcome.update_layout(xaxis={'categoryorder':'category ascending'})


# Load CSS Style
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Navigation Bar
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("Team-3 COVID-19 Dashboard", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://github.com/tenley8/Team-3",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

# Cases in Toronto
TORONTO_CASE = dbc.Card(
    [
        dbc.CardHeader(html.H5("Toronto COVID-19 - Number of Cases")),
        dbc.CardBody([
            dcc.Tabs(
                id="tabs1",
                children=[
                    dcc.Tab(
                        label="Age Group",
                        children=[
                            dcc.Graph(id='toronto_case_by_age'),
                        ]
                    ),
                    dcc.Tab(
                        label="Gender",
                        children=[dcc.Graph(id="toronto_case_by_gender", figure=fig_gender)]
                    )
                ]
            ),
            html.Label("Select Date Since the First Case", style={"marginTop": 10}, className="lead"),
            dcc.Slider(
                id='date-slider',
                min=toronto_df['date_since_first_case'].min(),
                max=toronto_df['date_since_first_case'].max(),
                value=toronto_df['date_since_first_case'].max(),
                marks={str(date): str(date) for date in pd.Series(np.arange(0,toronto_df['date_since_first_case'].max(),5))},
                step=None
            )
        ])
    ]        
)

TORONTO_OUTCOME = dbc.Card(
    [
        dbc.CardHeader(html.H5("Toronto COVID-19 - Outcomes")),
        dbc.CardBody(
            dcc.Tabs(
                id="tabs2",
                children=[
                    dcc.Tab(
                        label="Age Group",
                        children=[dcc.Graph(id="toronto_outcome_by_age", figure=fig_age_outcome)]
                    ),
                    dcc.Tab(
                        label="Gender"
                    )
                ]
            )
        )
    ]        
)

BODY = dbc.Container(
    [
        dbc.Col(dbc.Card(TORONTO_CASE), style={"marginTop": 20}),
        dbc.Col(dbc.Card(TORONTO_OUTCOME), style={"marginTop": 20})
    ]
)

app.layout = html.Div(children=[NAVBAR, BODY])


@app.callback(
    Output('toronto_case_by_age', 'figure'),
    [Input('date-slider', 'value')])
def update_figure(selected_date):
    filtered_df = toronto_df[toronto_df.date_since_first_case <= selected_date]

    fig = px.histogram(filtered_df, x="age_group", y="outcome", histfunc="count")

    fig.update_layout(transition_duration=500)

    return fig

# Running Application
if __name__ == '__main__':
    app.run_server(debug=True)