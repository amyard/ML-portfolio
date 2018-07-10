import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd
# solve the problem with
#ImportError: cannot import name 'is_list_like'
pd.core.common.is_list_like = pd.api.types.is_list_like

import pandas_datareader.data as web
from datetime import datetime

app = dash.Dash()

# load data with list of symbols and companies name
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace = True)
options = []

for i in nsdq.index:
    my_dict = {}
    my_dict['label'] = nsdq.loc[i]['Name']
    my_dict['value'] = i
    options.append(my_dict)


app.layout = html.Div([
        html.H1('Stock Ticker Dashboard'),
        html.Div([
                html.H3('Enter a stock symbol:', style = {'paddingRight':'30px'}),
                dcc.Dropdown(id = 'my_stock_picker',
                        options = options,
                        value = ['TSLA'],
                        multi = True  # choose many values
        )], style = {'display':'inline-block','verticalAlign':'top', 'width':'30%'}),
        html.Div([html.H3('Select a start and end date:'),
                  dcc.DatePickerRange(id='my_date_picker',
                                      min_date_allowed = datetime(2015,1,1),
                                      max_date_allowed = datetime.today(),
                                      start_date = datetime(2018,1,1),
                                      end_date = datetime.today())],
        style = {'display':'inline-block'}),
        html.Div([
                html.Button(id = 'submit-button',
                            n_clicks = 0,
                            children = 'Submit',
                            style = {'fontSize':24,'marginleft':'30px'})
        ], style = {'display':'inline-block'}),

        dcc.Graph(id = 'my_graph',
                figure = {'data':[
                            {'x':[1,2], 'y':[3,1]}
                ],
                          'layout' : {'title':'Default Title'}})
])


@app.callback(Output('my_graph', 'figure'),
             [Input('submit-button','n_clicks')],
             [State('my_stock_picker', 'value'),
                   State('my_date_picker','start_date'),
                   State('my_date_picker', 'end_date')])

def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'iex', start, end)
        traces.append({'x':df.index, 'y':df['close'], 'name': tic})

    fig = {'data':traces,
           'layout':{'title':stock_ticker}}
    return fig

if __name__ == '__main__':
    app.run_server()
