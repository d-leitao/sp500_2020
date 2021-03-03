import pandas as pd
import plotly.express as px
from scrapers import *


def growth_ts(top, summ_sorted, cum_growth_long):

    og_top = top
    if top == 'all':
        top = summ_sorted.shape[0]
        
    max_weight = summ_sorted.loc[top-1, 'Weight']

    fig = px.line(cum_growth_long.loc[cum_growth_long.Weight >= max_weight,:], 
        x='Date', y='Cum_Growth', color='Industry', line_group='Ticker',
        hover_data=['Security', 'Ticker', 'Industry', 'Date', 'Cum_Growth'],
        labels={'Weight': '<b>Weight</b>', 'Cum_Growth': '<b>Cumulative Growth</b>'},
        title='<b>S&P 500 Index (2020)</b>' if og_top=='all' else f'<b>Top {top} by Market Cap - S&P 500 Index (2020)</b>',
        width=1000, height=600)
    fig.update_traces(line=dict(width=1))
    fig.update_yaxes(tickformat="%")
    fig.update_layout(margin=dict(l=100, r=80, t=80, b=80))

    return fig


def growth_by_weight(cum_growth_long):

    fig = px.scatter(cum_growth_long.loc[cum_growth_long.Date=='2020-12-31',], 
        x='Weight', y='Cum_Growth', size='Weight', color='Industry',
        hover_data=['Security', 'Ticker', 'Industry', 'Date', 'Cum_Growth'],
        labels={'Weight': '<b>Weight</b>', 'Cum_Growth': '<b>Growth</b>'},
        title='<b>Individual Growth of Stocks in the S&P 500 Index <br>vs. Market Cap Weight (2020)</b>',
        width=800, height=600)

    fig.update_yaxes(tickformat="%")
    fig.update_xaxes(tickformat="%")
    fig.update_layout(margin=dict(l=100, r=80, t=100, b=80))
    
    return fig