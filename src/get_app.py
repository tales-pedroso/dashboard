# -*- coding: utf-8 -*-
import dash
from dash import html, dcc
import plotly.express as px

def get_app(dashboard_df, geojson):
    fig = px.choropleth(dashboard_df, 
                        geojson = geojson,
                        color = 'total_expense',
                        locations = 'state_',
                        featureidkey = 'properties.district',
                        projection = 'mercator')
    
    fig.update_geos(fitbounds = "locations", visible = False)
    fig.update_layout(margin={"r": 0,"t": 0,"l": 0,"b": 0})
    fig.show()

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure = fig)
    ])
    
    return app

'''
# bar plot
fig = px.bar(data_frame = dashboard_df, 
                 x = 'state_',
                 y = 'total_expense')
'''