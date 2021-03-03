import pandas as pd
import plotly.express as px
from scrapers import *


cblind = {'Consumer Discretionary': '#E69F00', 'Financials': '#000000',
          'Industrials': '#948A8A', 'Materials': '#DC3220',
          'Utilities': '#56B4E9', 'Real Estate': '#009E73', 'Energy': '#332288', 
          'Information Technology': '#0072B2', 'Health Care': '#FF008D', 
          'Communication Services': '#D55E00', 'Consumer Staples': '#F0E442'}


def growth_ts(top, summ_sorted, cum_growth_long):

    og_top = top
    if top == 'all':
        top = summ_sorted.shape[0]
        
    max_weight = summ_sorted.loc[top-1, 'Weight']

    fig = px.line(cum_growth_long.loc[cum_growth_long.Weight >= max_weight,:], 
        x='Date', y='Cum_Growth', color='Industry', line_group='Ticker',
        hover_data=['Security', 'Ticker', 'Industry', 'Date', 'Cum_Growth'],
        color_discrete_map=cblind,
        labels={'Weight': '<b>Weight</b>', 'Cum_Growth': '<b>Cumulative Growth</b>'},
        title='<b>S&P 500 Index (2020)</b>' if og_top=='all' else f'<b>Top {top} by Market Cap - S&P 500 Index (2020)</b>',
        width=1000, height=600)
    fig.update_traces(line=dict(width=1))
    fig.update_yaxes(tickformat="%")
    fig.update_layout(margin=dict(l=100, r=80, t=80, b=80))

    return fig


def growth_by_weight(growth_weight_df, industry=False):

    fig = px.scatter(growth_weight_df, 
        x='Weight', y='Growth', size='Weight', color='Industry',
        hover_data=['Industry', 'Growth', 'Weight'] if industry
            else ['Security', 'Ticker', 'Industry', 'Growth', 'Weight'],
        color_discrete_map=cblind,
        labels={'Weight': '<b>Weight</b>', 'Growth': '<b>Growth</b>'},
        title= '<b>S&P 500 Index Industry Growth <br>vs. Industry Market Cap Weight (2020)</b>'if industry
            else '<b>Individual Growth of Stocks in the S&P 500 Index <br>vs. Market Cap Weight (2020)</b>',
        width=1000, height=600)

    fig.update_yaxes(tickformat="%")
    fig.update_xaxes(tickformat="%")
    fig.update_layout(margin=dict(l=100, r=80, t=100, b=80))
    
    return fig