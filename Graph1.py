from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from plotly_calplot import calplot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# create the dataframe
df = pd.read_csv('activities_clean.csv')

# converts the 'start_date' column to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])

# create fig1: strava activities distance (m)
fig1 = px.scatter(df, x='start_date', y='distance', color='type', title='Strava activities distance (m)')
fig1.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# create fig2: Strava activities averate speed (km/h)
fig2 = px.scatter(df, x='start_date', y='average_speed', color='type', title='Strava activities averate speed (km/h)')

fig2.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# create fig3: calendar heatmap daily activities number
# Create the df_cal dataframe with the start_date and counts column from df values
df_cal = df['start_date'].value_counts().rename_axis('start_date').reset_index(name='counts')
# Sort the dataframe by the 'start_date' column in ascending order and update the dataframe in place
df_cal.sort_values(by='start_date', inplace=True)
# calendar heatmap
fig3 = calplot(df_cal, x="start_date", y="counts", years_title=True, colorscale="blues", gap=4)


app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Strava Data'),
        html.Div(children='Using Dash/Plotly to visualize Strava Activity Data.'),
        html.Div(children='This Dashboard is linked to the following repository:'),
        dcc.Link(children='https://github.com/MakeRollMake/Dash_test_render', href='https://github.com/MakeRollMake/Dash_test_render'),
        dcc.Graph(id='graph1', figure=fig1),
        dcc.Graph(id='graph2', figure=fig2),
        dcc.Graph(id='graph3', figure=fig3)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
