import json
import requests
import pandas as pd
import numpy as np

#pd.options.mode.chained_assignment = None  # default='warn'

"""
SEC SERVER LIMIT PROBLEM
cik = '0001326380'
base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'
company_data = requests.get(base_url.format(cik)).json()
"""

company_file = open('CIK0001326380.json',)
account_name = input('Enter account name: ')

def account_tracker(account):
    """
    For a chosen account (e.g., amortization of intangible assets), the function
    converts (from .json to pandas dataframe), cleans, and tracks its historical data.
    """
    
    data = json.load(company_file)
    account_root = data['facts']['us-gaap'][account] #set a base path directory

    print(account_root['label']) #account name
    print(account_root['description']) #account info

    #create an empty dataframe
    account_data = pd.DataFrame() 

    #comb through account's quarters (starting ~2008Q2)
    for data in account_root['units']['USD']:
        df = pd.DataFrame(data, index=[0]) #df temporarily stores all of current quarter's data
        df1 = df[df.columns.difference(['end', 'accn', 'fy', 'fp', 'form', 'filed'])] #remove unwanted columns
        account_data = account_data.append(df1) #append remaining two columns to the initially empty dataframe 
    
    account_data = account_data.dropna() #remove repeated values (e.g., Q4 data = 10k data)
    account_data = account_data.rename(columns={"val": "value", "frame": "date"})
    account_data = account_data.reset_index(drop=True) #label rows numerically
    account_data['date'] = account_data['date'].map(lambda x: x.lstrip('cCyY').rstrip('iI')) #remove substrings in column
    
    return account_data

print(account_tracker(account_name))



