import yfinance as yf
import yahoo_fin.stock_info as si
from vega_datasets import data

import pandas as pd
import datetime as dt


import altair as alt
import streamlit as st

import requests
import matplotlib as plt


st.title('US Stock Market3')

symbols = si.tickers_sp500()
tickers = st.sidebar.multiselect(
     'Choose a S&P 500 Stock',
     symbols, 
     default=['MO', 'IBM', 'XOM', 'CVX', 'T', 'ABBV', 'VZ', 'KO', 'MMM', 'PG','JNJ']
     ,)

#Main
'''
Price Fluctuations
'''
###Price fluctuations

def tabulate_fluc(tickers):
    fluc_tab = pd.DataFrame()

    for tkr in tickers:
        quote = pd.DataFrame([si.get_quote_table(tkr)])
        quote = quote.transpose().reset_index(inplace=False).rename(columns={'index': 'Attribute', 0: "Value"})
        price = quote.iloc[[12,0,1],:]
        stats = si.get_stats(tkr).iloc[[5,6,1],:]
        p_fluc = price.append(stats).set_index('Attribute').rename(columns={'Value': tkr})
        
        #dataframe = dataframe.rename(columns={'Value': tkr})
        each = p_fluc[[tkr]]
        each = each.T#.iloc[[0],:]
        #divi_tab = ori.append(each)
        fluc_tab = pd.concat([fluc_tab,each])
    return fluc_tab.T
st.write(tabulate_fluc(tickers))

'''

Dividend
'''
def tabulate_divi(tickers):
    divi_tab = pd.DataFrame()
    for tkr in tickers:
        dividend = si.get_stats(tkr).iloc[[20,26,24],:].set_index('Attribute')
        dividend = dividend.rename(columns={'Value': tkr})
        #dataframe = dataframe.rename(columns={'Value': tkr})
        each = dividend[[tkr]]
        each = each.T#.iloc[[0],:]
        #divi_tab = ori.append(each)
        divi_tab = pd.concat([divi_tab,each])
    return divi_tab.T
st.write(tabulate_divi(tickers))

'''

Fundamental
'''

def tabulate_fund(tickers):
    fund_tab = pd.DataFrame()

    for tkr in tickers:
        f_quote1 = pd.DataFrame([si.get_quote_table(tkr)])
        f_quote1 = f_quote1.transpose().reset_index(inplace=False).rename(columns={'index': 'Attribute', 0: 'Value'})
        f_per = f_quote1.iloc[[13],:]

        stats1 = si.get_stats(tkr).iloc[[34,49,50],:]

        f_valu = si.get_stats_valuation(tkr)
        f_valu = f_valu.rename(columns={0: 'Attribute', 1: 'Value'}).iloc[[0,6],:]
        fund_d = f_valu.append(f_per).append(stats1).set_index('Attribute').rename(columns={'Value': tkr})
        
        each = fund_d[[tkr]]
        each = each.T#.iloc[[0],:]
        #divi_tab = ori.append(each)
        fund_tab = pd.concat([fund_tab,each])
    return fund_tab.T
st.write(tabulate_fund(tickers))

'''
BUY < 15 < SELL
'''


#ColorSet
#CandleStickChart
#Parameters
StartDate = '2010-01-01'
base =[]
ticker =[]
source = []


def lineup(ticker):
    stock_data = si.get_data(ticker,StartDate)
    stock_data.index.name = 'date'
    stock_data.index.strftime('%d %B %Y')
    stock_data = stock_data.reset_index()

    #Method1
    base = alt.Chart(stock_data).encode(
        alt.X('date:T', 
            axis=alt.Axis(labelAngle=-45)        
        ),
        color = alt.condition("datum.open <= datum.close",
             alt.value("#06982d"),
            alt.value("#ae1325")
        )
        )

    CandleChart = alt.layer(
        base.mark_rule().encode(
            alt.Y('low:Q',
                title='Stock Prices(USD)', 
                scale=alt.Scale(zero=False)
            ), 
            alt.Y2('high:Q')
        ),
        base.mark_bar().encode(alt.Y('open:Q'), alt.Y2('close:Q')),
    ).interactive()
    return st.altair_chart(CandleChart, use_container_width=True) 

 
for tkr in tickers:
    price = round(si.get_live_price(tkr),2)
    st.write(f"""
    ## **{tkr}**  
    ## {price} USD 
    """)
    lineup(ticker=tkr)

    tckr = yf.Ticker(tkr)
    reco = tckr.recommendations
    reco.index = reco.index.strftime('%Y/%m/%d')
    st.write(reco.tail(5))


