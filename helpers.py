import requests, json

from sqlalchemy import true


def transactions():
  """Get and break down data into a dict for easy searching"""
  r = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json')
  transactions = r.text
  trans_dict = json.loads(transactions)
  for trans in trans_dict:
    if 'John' in trans['representative']:
      print('works')
      print(trans)
  # print(trans_dict)
  return trans_dict

def search_by_name(first, last):
  r = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json')
  reps = set(())
  transactions = r.text
  trans_dict = json.loads(transactions)
  for trans in trans_dict:
    if first in trans['representative']:
      reps.add(trans['representative'])
   
  return reps

# {
#   'disclosure_year': 2020,
#   'disclosure_date': '01/10/2020',
#   'transaction_date': '2019-12-06',
#   'owner': None,
#   'ticker': 'ADS',
#   'asset_description': 'Alliance data Systems Corporation',
#   'type': 'sale_full', 
#   'amount': '$1,001 - $15,000',
#   'representative': 'Hon. Gilbert Cisneros',
#   'district': 'CA39',
#   'ptr_link':
#   'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2020/20013867.pdf',
#   'cap_gains_over_200_usd': False
#   },