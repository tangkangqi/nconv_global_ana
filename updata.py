import os, sys
import requests
import pandas as pd


def update_data():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    fname = url.split('/')[-1]
    with open(fname, 'w') as f:
        r = requests.get(url)
        req = r.text
        f.write(req)
def ana():
    df = pd.read_csv('time_series_19-covid-Confirmed.csv')
    print(df)

if __name__ == '__main__':
    update_data()
    ana()

