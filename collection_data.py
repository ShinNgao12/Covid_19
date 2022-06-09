import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import datetime


header = ['#', 'Country,Other', 'TotalCases','NewCases','TotalDeaths','NewDeaths',
              'TotalRecovered' , 'NewRecovered' , 'ActiveCases' , 'Serious,Critical' , 
              'Tot Cases/1M pop', 'Deaths/1M pop', 'TotalTests', 'Tests/1M pop', 'Population',
              'Continent', 'New Cases/1M pop', 'New Deaths/1M pop', 'Active Cases/1M pop'] 

url =  'https://www.worldometers.info/coronavirus/'

def collect_2days_ago():
    while True:
        data_dict = {}
        for i in header:
            data_dict[i] = [] 
            
        
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'html5lib')
        source = soup.find('table', {'id' :"main_table_countries_yesterday2"})
        data = source.tbody.text

        # tách dữ liệu, dữ liệu thu được về khác nhau ở các lần crawl
        try:
            data = data.split('\n'*13)[-1]
        except:
            str_split = str('\n'*12) + ' \n'
            data = data.split(str_split)[-1]

        # chuyển dữ liệu thành dictionary 
        lines = data.split('\n')
        idx = 0
        while (idx < len(lines)):
            att = idx % 23
            if att in [16,17,21,22]:
                idx += 1
                continue
            elif lines[idx] == '' or lines[idx] == 'N/A':
                if att > 15:
                    data_dict[header[att - 2]].append(np.nan)
                    idx += 1
                else:
                    data_dict[header[att]].append(np.nan)
                    idx += 1
            else:
                if att > 15 :
                    data_dict[header[att - 2]].append(lines[idx])
                    idx += 1
                else:
                    data_dict[header[att]].append(lines[idx])
                    idx += 1
        
        length = min([len(v) for k, v in data_dict.items()])
        if len(data_dict['#']) == length and data_dict['#'][-1] != np.nan:
            break
        
        del data_dict
        time.sleep(0.5)
        
    return data_dict


def collect_yesterday():
    while True:
        data_dict = {}
        for i in header:
            data_dict[i] = []  

        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'html5lib')
        source = soup.find('table', {'id' :"main_table_countries_yesterday"})
        data = source.tbody.text

        # tách dữ liệu, dữ liệu thu được về khác nhau ở các lần crawl
        try:
            data = data.split('\n'*13)[-1]
        except:
            str_split = str('\n'*12) + ' \n'
            data = data.split(str_split)[-1]

        # chuyển dữ liệu thành dictionary 
        lines = data.split('\n')
        idx = 0
        while (idx < len(lines)):
            att = idx % 23
            if att in [16,17,21,22]:
                idx += 1
                continue
            elif lines[idx] == '' or lines[idx] == 'N/A':
                if att > 15:
                    data_dict[header[att - 2]].append(np.nan)
                    idx += 1
                else:
                    data_dict[header[att]].append(np.nan)
                    idx += 1
            else:
                if att > 15 :
                    data_dict[header[att - 2]].append(lines[idx])
                    idx += 1
                else:
                    data_dict[header[att]].append(lines[idx])
                    idx += 1
                    
        length = min([len(v) for k, v in data_dict.items()])
        if len(data_dict['#']) == length and data_dict['#'][-1] != np.nan:
            break
            
        del data_dict
        time.sleep(0.5)
        
    return data_dict


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

yesterday_dict = collect_yesterday()
yesterday_df = pd.DataFrame(yesterday_dict).set_index('#')
yesterday_df['Date'] = yesterday
yesterday_df.replace(' ', np.nan, inplace = True)
yesterday_df.to_csv(f'Data/data-covid_{str(yesterday)}.csv', index = False)

two_days_ago = today - datetime.timedelta(days=2)
two_days_ago_dict = collect_2days_ago()
two_days_ago_df = pd.DataFrame(two_days_ago_dict).set_index('#')
two_days_ago_df['Date'] = two_days_ago
two_days_ago_df.replace(' ', np.nan, inplace = True)
two_days_ago_df.to_csv(f'Data/data-covid_{str(two_days_ago)}.csv', index = False)