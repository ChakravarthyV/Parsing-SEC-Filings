import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

"""
SEC SERVER LIMIT PROBLEM
cik = '0001326380'
base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'
company_data = requests.get(base_url.format(cik)).json()
"""

company_file = open('CIK0001326380.json',)
account_name = input('Enter account name: ')

def account_storage(account):
    """
    For a chosen account (e.g., amortization of intangible assets), the function
    converts (from .json to pandas df), cleans, and stores its historical data.
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
    account_data = account_data.rename(columns={"val": "Amount ($)", "frame": "Year"}) #change column names
    account_data = account_data.reset_index(drop=True) #label rows numerically
    account_data['Year'] = account_data['Year'].map(lambda x: x.lstrip('cCyY').rstrip('iI')) #remove substrings in column
    
    return account_data #quarterly data

def account_stats():
    """
    Presents YoY change in account data (as a bar graph). 
    """
    
    account = account_storage(account_name) #quarterly df from account_storage function
    quarters = ['1', '2', '3', '4']
    quarter_choice = input('Quarter of choice: ')
    
    for quarter in quarters:
        if quarter != quarter_choice:
            account = account[~account.Year.str.contains('Q' + quarter)] #removes e.g. Q1/2/3 data if Q4 chosen
    account['Year'] = account['Year'].str[2:] #remove 20---- from e.g. 2008Q2
    
    ax = account.plot(kind='bar', title=account_name, x='Year', y='Amount ($)')
    
    return ax

print(account_stats())



