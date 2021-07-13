import json
import requests
import pandas as pd #from here on out, df refers to a pandas dataframe
import matplotlib.pyplot as plt

"""
SEC SERVER LIMIT PROBLEM
cik = '0001326380'
base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'
company_data = requests.get(base_url.format(cik)).json()
"""

company_file = open('CIK0001326380.json',)
num_of_accounts = int(input('How many accounts would you like to track? [MIN 1] '))
accounts_chosen = [] #stores user's list of accounts to track
for num in range(num_of_accounts):
    accounts_chosen.append(input()) #requests user to enter account (GAAP-formated)
data_file = json.load(company_file)


def account_storage(account, data):
    """
    For a chosen account (e.g., amortization of intangible assets), the function
    converts (from .json to pandas df), cleans, and stores its historical data.
    """
    
    account_root = data['facts']['us-gaap'][account] #set a base path directory

    print(account_root['label']) #account name
    print(account_root['description']) #account info

    #create an empty df
    account_data = pd.DataFrame() 

    #comb through account's quarters (starting ~2008Q2)
    for data in account_root['units']['USD']:
        df = pd.DataFrame(data, index=[0]) #df temporarily stores all of current quarter's data
        df1 = df[df.columns.difference(['end', 'accn', 'fy', 'fp', 'form', 'filed'])] #remove unwanted columns
        account_data = account_data.append(df1) #append remaining two columns to the initially empty dataframe 
    
    account_data = account_data.dropna() #remove repeated values (e.g., Q4 data = 10k data)
    account_data = account_data.rename(columns={"val": account + " ($)", "frame": "Year"}) #change column names
    account_data = account_data.reset_index(drop=True) #label rows numerically
    account_data['Year'] = account_data['Year'].map(lambda x: x.lstrip('cCyY').rstrip('iI')) #remove substrings in column
    
    return account_data #quarterly data

def account_stats():
    """
    Presents YOY change in accounts (as bar graphs). 
    """
    #choose stacked vs. unstacked bar graph 
    bar_graph_type = int(input('Bar Graph(s) Type [enter #]: \n 1. Stacked \n 2. Unstacked \n'))
    
    accounts_as_df = [] #empty list to store accounts as df's 
    
    for account in accounts_chosen:
        #add account df to empty list by calling account_storage function
        accounts_as_df.append(account_storage(account, data_file)) 
    
    all_accounts = pd.concat(accounts_as_df, axis=1) #concatenate all dataframes in the list
    all_accounts = all_accounts.loc[:,~all_accounts.columns.duplicated()] #remove year column since it's repeated

    quarters = ['1', '2', '3', '4']
    quarter_choice = input('Quarter of choice: ')
    
    for quarter in quarters:
        if quarter != quarter_choice:
            #removes e.g. Q1/2/3 data if Q4 chosen
            all_accounts = all_accounts[~all_accounts.Year.str.contains('Q' + quarter, na=False)] #ignore NaN values
    all_accounts['Year'] = all_accounts['Year'].str[2:] #remove 20---- from e.g. 2008Q2
    
    ax = all_accounts.plot(kind='bar', title='Year-Over-Year Performance', x='Year')
    
    return ax

print(account_stats())



