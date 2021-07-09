import json
import requests
import pandas as pd

"""
FIGURE A WAY AROUND SEC SERVER LIMIT
cik = '0001326380'
base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'
company_data = requests.get(base_url.format(cik)).json()
"""
company_file = open('CIK0001326380.json',)
account = input('Enter accounting figure: ')

data = json.load(company_file)

account_root = data['facts']['us-gaap'][account]

print(account_root['label'])
print(account_root['description'])

#store all relevant figures under the chosen account
account_data = pd.DataFrame()
for data in account_root['units']['USD']:
    df = pd.DataFrame(data, index=[0])
    account_data = account_data.append(df)
print(account_data)
    



