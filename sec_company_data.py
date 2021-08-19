import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

#convert company's json file into pandas dataframe
company_file = open('CIK0001326380.json',)
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
    
    return account_data #quarterly data, cleaned

def account_yoy_change(accounts_list):
    """
    Presents YOY change in accounts (as bar graphs). Assumes accounts_list is a clean list of quarterly account data.
    """
    #choose stacked vs. unstacked bar graph 
    #bar_graph_type = int(input('Bar Graph(s) Type [enter #]: \n 1. Stacked \n 2. Unstacked \n'))
    
    all_accounts = pd.concat(accounts_list, axis=1) #concatenate all dataframes in the list
    all_accounts = all_accounts.loc[:,~all_accounts.columns.duplicated()] #remove year column since it's repeated
    print(all_accounts)
    quarters = ['1', '2', '3', '4']
    quarter_choice = input('Quarter of choice: ')
    
    for quarter in quarters:
        if quarter != quarter_choice:
            #removes e.g. Q1/2/3 data if Q4 chosen
            all_accounts = all_accounts[~all_accounts.Year.str.contains('Q' + quarter, na=False)] #ignore NaN values
    all_accounts['Year'] = all_accounts['Year'].str[2:] #remove 20---- from e.g. 2008Q2
    
    ax = all_accounts.plot(kind='bar', title='Year-Over-Year Performance', x='Year')
    
    return ax

#Profitability Ratios
def roa():
    """
    Calculates Return on Assets. Here, ROA = [Net Income + Interest Expenses(1 - Tax Rate)]/Total Assets.
    in json: operatingincomeloss(1-.21)/Assets
    """
    #manage appropriate accounts
    operating_income = account_storage('OperatingIncomeLoss', data_file)
    operating_income['OperatingIncomeLoss ($)'] = operating_income['OperatingIncomeLoss ($)'].multiply(1-0.21) #adjust for corporate tax (21%)
    total_assets = account_storage('Assets', data_file)
    
    operating_income = operating_income[~operating_income['Year'].str.contains("Q")] #remove rows that contain quarterly data
    operating_income = operating_income.reset_index(drop=True) #label rows numerically
    
    #take average of assets as recorded in quarters of a year, and label new columns accordingly
        
#user chooses accounts to clean and track
print("Enter accounts you would like to track. Type 'Q' to quit.")
accounts = [] #stores processed collection of chosen accounts
while True:
    choice = input('Account: ')
    if choice.lower() == 'q':
        break
    else:
        accounts.append(account_storage(choice, data_file)) 
        
print(account_yoy_change(accounts))