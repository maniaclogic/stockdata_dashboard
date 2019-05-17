import dash
import dash_core_components as dcc
import dash_html_components as html
import iexfinance as finance
from iexfinance.stocks import get_historical_data
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go

public_token = 'pk_027ce70b2a994d169bcac0a0da2fdcdd'

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

df = get_historical_data('DAX', start=start, end=end, output_format='pandas', token=public_token)

trace_close = go.Scatter(x=list(df.index),
                         y=list(df.close),
                         name='Close',
                         line=dict(color='#006666'))

data = [trace_close]

layout = dict(title='DAX chart',
              showlegend=False)

fig = dict(data=data, layout=layout)

app = dash.Dash()

app.layout = html.Div([
    html.H1(children='Stock Data Dashboard'),
    html.Label('DAX Chart'),
    html.Div(
        dcc.Input(
            id='stock-input',
            placeholder='Enter a Stock to get tickers',
            type='text',
            value=''
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

    html.Div(
        dcc.Graph(id='DAX chart',
                  figure=fig)
    )
])

if __name__=="__main__":
    app.run_server(debug=True)
