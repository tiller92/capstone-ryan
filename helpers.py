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
