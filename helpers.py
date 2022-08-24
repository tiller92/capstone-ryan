from psycopg2 import Timestamp
import requests, json

from sqlalchemy import false, true


def transactions():
  """Get and break down data into a dict for easy searching"""
  r = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json')
  transactions = r.text
  trans_dict = json.loads(transactions)
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


def filterByTransactionDate(list):
  """recieves a list and orders by transaction date using a merge sort """
#sorts by year then month then day
  
  n = len(list)
  for i in range(n):
    swapped = False
    for j in range(0,n-i-1):
      arr = list[j]['transaction_date'].split('-')
      year = int(arr[0])
      month = int(arr[1])
      day = int(arr[2])
      
      arr2 = list[j + 1]['transaction_date'].split('-')
      year2 = int(arr2[0])
      month2 = int(arr2[1])
      day2 = int(arr2[2])
      if year > year2:
        temp = list[j+1]
        list[j+1] = list[j]
        list[j] = temp
        swapped =True
    if swapped == False:
          break

  
  # Now this filters by month
  n = len(list)
  for i in range(n):
    swapped = False
    for j in range(0,n-i-1):
      arr = list[j]['transaction_date'].split('-')
      year = int(arr[0])
      month = int(arr[1])
      day = int(arr[2])
      
      arr2 = list[j + 1]['transaction_date'].split('-')
      year2 = int(arr2[0])
      month2 = int(arr2[1])
      day2 = int(arr2[2])
      if year == year2 and month > month2:
        temp = list[j+1]
        list[j+1] = list[j]
        list[j] = temp
        swapped =True
    if swapped == False:
          break
  
  #  this filters by day      
  n = len(list)
  for i in range(n):
    swapped = False
    for j in range(0,n-i-1):
      arr = list[j]['transaction_date'].split('-')
      year = int(arr[0])
      month = int(arr[1])
      day = int(arr[2])
      
      arr2 = list[j + 1]['transaction_date'].split('-')
      year2 = int(arr2[0])
      month2 = int(arr2[1])
      day2 = int(arr2[2])
      if year == year2 and month == month2 and day > day2:
        temp = list[j+1]
        list[j+1] = list[j]
        list[j] = temp
        swapped =True
    if swapped == False:
          break
  return list