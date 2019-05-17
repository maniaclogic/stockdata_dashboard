import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from iexfinance.stocks import get_historical_data
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go

public_token = 'pk_ca63b49cdbb34875ab21176ec50e99c6'

start = datetime.datetime.today() - relativedelta(days=5)
end = datetime.datetime.today()

df1 = get_historical_data('AMZN', start=start, end=end, output_format='pandas', token=public_token)



trace_close1 = go.Scatter(x=list(df1.index),
                         y=list(df1.close),
                         name='Close',
                         line=dict(color='#006666'))

data1 = [trace_close1]


layout1 = dict(title='Amazon chart',
              showlegend=False)


fig1 = dict(data=data1, layout=layout1)



app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H2('Stock Data Dashboard'),
        html.Img(src='/assets/stock-icon.png'),
        ], className='banner'),
    html.Label('Financial Stock Charting'),
    html.Div(
        dcc.Input(
            id='stock-input',
            type='text',
            value='SPY'
        ),
    ),

    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Candlestick', 'value': 'Candlestick'},
                {'label': 'Line', 'value': 'Line'}
            ]
        )
    ),

    html.Div([
        html.Div([
            dcc.Graph(id='chart',)
        ], className='six columns'),
        html.Div([
            dcc.Graph(id='Amazon chart',
                      figure=fig1)
        ], className='six columns')
    ], className='row')
])

app.css.append_css({
    'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(dash.dependencies.Output('chart', 'figure'),
                  [dash.dependencies.Input('stock-input', 'value')])

def update_fig(input_value):
    df = get_historical_data(input_value, start=start, end=end, output_format='pandas', token=public_token)

    data =[]
    trace_close = go.Scatter(x=list(df.index),
                             y=list(df.close),
                             name='Close',
                             line=dict(color='#006666'))
    data.append(trace_close)
    layout = dict(title='Callback_Graph',
                  showlegend=False)
    value = {'data': data, 'layout': layout}

    return value

if __name__=="__main__":
    app.run_server(debug=True)
