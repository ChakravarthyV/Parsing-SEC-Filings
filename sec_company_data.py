import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

#open and read json file
company_file = open('apple_json.json',)
data_file = json.load(company_file)

def json_to_pd(account):
    """
    For a chosen account (e.g., amortization of intangible assets), the function
    converts (from .json to pandas df), cleans, and stores its historical quarterly data.
    """
    account_root = data_file['facts']['us-gaap'][account] #set a base path directory

    print(account_root['label']) #account name
    print(account_root['description']) #account info

    #create an empty df
    account_data = pd.DataFrame() 

    #comb through account's quarters
    for data in account_root['units']['USD']:
        df = pd.DataFrame(data, index=[0]) #df temporarily stores all of current quarter's data
        df1 = df[df.columns.difference(['end', 'accn', 'fy', 'fp', 'form', 'filed'])] #remove unwanted columns
        account_data = account_data.append(df1) #append remaining two columns to the initially empty dataframe 
    
    account_data = account_data.dropna() #remove repeated values (e.g., Q4 data = 10k data) 
    account_data = account_data.rename(columns={"val": account, "frame": "Year"}) #change column names
    account_data = account_data.reset_index(drop=True) #label rows numerically
    account_data['Year'] = account_data['Year'].map(lambda x: x.lstrip('cCyY').rstrip('iI')) #remove substrings in column
    
    return account_data #returns quarterly data as a pandas df

#global variables [parses through the recent quarter report]
cash = json_to_pd('CashAndCashEquivalentAtCarryingValue')['CashAndCashEquivalentAtCarryingValue'].iloc[-1]
receivables = json_to_pd('AccountsReceivableNetCurrent')['AccountsReceivableNetCurrent'].iloc[-1]
inventories = json_to_pd('InventoryNet')['InventoryNet'].iloc[-1]
current_prepaid = json_to_pd('OtherPrepaidExpenseCurrent')['OtherPrepaidExpenseCurrent'].iloc[-1]

current_assets = json_to_pd('AssetsCurrent')['AssetsCurrent'].iloc[-1]

non_current_prepaid = json_to_pd('PrepaidExpenseOtherNoncurrent')['PrepaidExpenseOtherNoncurrent'].iloc[-1]
ppe = json_to_pd('PropertyPlantAndEquipmentNet')['PropertyPlantAndEquipmentNet'].iloc[-1]
goodwill = json_to_pd('Goodwill')['Goodwill'].iloc[-1]

total_liabilities = json_to_pd('Liabilities')['Liabilities'].iloc[-1] #taken at face value

def liquidation_value():
    """
    Assumes liquidation is immediate (< 3 years). Returns a conservative estimate
    that should, in theory, provide a floor to a firm's fundamental value. In most cases, it will be
    negative since it assumes a worst case scenario where assets reported are difficult to sell and 
    all the liabilities are taken at face value.
    """    
    receivables_writedown = receivables*0.15 #takes the last element of receivables column and gives it a 15% writedown
    inventories_writedown = inventories*0.50 #50% reduction
    
    adj_current_assets = current_assets - (receivables_writedown + inventories_writedown) #current assets adjusted for conservative writedowns
    
    adj_ppe = ppe*0.45 #reported ppe discounted by 45%
    
    adj_total_assets = adj_current_assets + adj_ppe
    
    liq_val = adj_total_assets - total_liabilities
    
    print(liq_val)

def adjusted_nav():
    """
    Allows the user to adjust reported accounts as he/she sees fit. The user-adjusted net asset value
    of the company is returned.
    """
    
print(json_to_pd('AssetsCurrent'))
print(liquidation_value())