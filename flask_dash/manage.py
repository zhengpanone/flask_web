# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/10 16:27
"""

# import lib
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

assert_folder = os.path.abspath('./app/static/')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.cs',
                        {
                            'src': os.path.join(assert_folder, 'favicon.ico'),
                            'rel': 'icon'
                        }
                        ]
app = dash.Dash(__name__, assets_folder=assert_folder, external_stylesheets=external_stylesheets)

all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/violin_data.csv")

app.layout = html.Div(children=[
    html.H1(children="Hello Dash"),
    html.Div(children="""
                                Dash: A web application framework for python
                                """),
    dcc.Graph(id='example-graph',
              figure={
                  'data': [

                      go.Violin(y=df['total_bill'], box_visible=True, line_color='black',
                                meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
                                x0='Total Bill')

                  ],
                  'layout': {
                      'title': 'Dash Data Visualization'
                  }
              })])

if __name__ == '__main__':
    app.run_server(debug=True)
