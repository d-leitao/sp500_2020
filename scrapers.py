import os
import pandas as pd
import pandas_datareader.data as pddr
import requests
from bs4 import BeautifulSoup as bs


def info_build(rescrape=False):

    if rescrape == False and os.path.exists('data/info.csv'):
        info_df = pd.read_csv('data/info.csv', index_col=0)
        return info_df

    # s&p 500 list on wikipedia, as of 2020/12/31
    resp = requests.get('https://en.wikipedia.org/w/index.php?title=List_of_S%26P_500_companies&oldid=997494787')
    soup = bs(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    row_lists = []
    for row in table.findAll('tr')[1:]:

        row_tds = row.findAll('td')

        ticker = row_tds[0].text[:-1]
        security = row_tds[1].text
        industry = row_tds[3].text
        date_added = row_tds[6].text

        row_lists.append([ticker, security, industry, date_added])

    info_df = pd.DataFrame(row_lists, columns=['ticker', 'security', 'industry', 'date_added'])
    # only companies that were in the index for the whole year
    info_df = (info_df
        .loc[~info_df.date_added.str.contains('2020'),:]
        .drop('date_added', axis='columns')
        .reset_index(drop=True))

    info_df.to_csv('data/info.csv')

    return info_df

def weights_build(rescrape):

    if rescrape == False and os.path.exists('data/weights.csv'):
        weights = pd.read_csv('data/weights.csv', index_col=0)
        return weights

    # s&p 500 individual weights as of 2020/12/20
    resp = requests.get('https://web.archive.org/web/20201220022904/https://www.slickcharts.com/sp500')
    soup = bs(resp.text, 'lxml')
    table = soup.find('table', {'class': 'table table-hover table-borderless table-sm'}).find('tbody')

    row_lists = []
    for row in table.findAll('tr'):
        
        ticker = row.findAll('td')[2].text
        weight = float(row.findAll('td')[3].text)

        row_lists.append([ticker, weight])

    weights = pd.DataFrame(row_lists, columns=['ticker', 'weight'])
    weights.to_csv('data/weights.csv')

    return weights


def summ_build(rescrape=False): #puts together info and weights

    if rescrape == False and os.path.exists('data/summ.csv'):
        summ = pd.read_csv('data/summ.csv', index_col=0)
        return summ

    i = info_build(rescrape)
    w = weights_build(rescrape)

    summ = i.merge(w, how='left', on='ticker')
    summ.weight = summ.weight / summ.weight.sum()
    
    if not summ[summ.isnull().any(axis=1)].empty: #missing weights
        print('There are missing weight values for the tickers in info!')
        
    summ.to_csv('data/summ.csv')

    return summ


def panel_build(rescrape=False): #scrapes ticker prices

    if rescrape == False and os.path.exists('data/panel.csv'):
        panel = pd.read_csv('data/panel.csv', index_col=0)
        return panel 

    summ = summ_build(rescrape)

    #yahoo tickers use dashes instead of points
    yahoo_tickers = [t.replace('.', '-') for t in summ.ticker]

    daily = pddr.DataReader(yahoo_tickers, 'yahoo', '2020-01-01', '2020-12-31')
    panel = daily['Adj Close']

    panel.columns = [t.replace('-', '.') for t in panel.columns]
    panel.Date = pd.to_datetime(panel.Date)

    panel.to_csv('data/panel.csv')
    
    return panel


def backups_build():

    for file in ['info', 'weights', 'summ', 'panel']:
        (pd.read_csv(f'data/{file}.csv', index_col=0)
        .to_csv(f'data/backups/{file}_backup.csv'))