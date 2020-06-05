import csv
import datetime
import requests
import json 

def processCSV(path, baseCurrency):
   target_doc = csv.reader(open(path), delimiter=",", quotechar='|')
   supportedCurrencies = ['CAD', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 'GBP', 'RON', 'SEK', 'IDR',
         'IDR', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 'CHF', 'EUR', 'MYR', 'BGN', 'TRY', 'CNY', 'NOK',
         'NZD', 'ZAR', 'USD', 'MXN', 'SGD', 'AUD', 'ILS', 'KRW', 'PLN']
   URL = "https://api.exchangeratesapi.io/latest"
   PARAMS = {'base':baseCurrency}
   try:
    r = requests.get(url = URL, params = PARAMS)
   except:
     raise "Exchange Rate API not working" 
   data = r.json()      
   resultRow = {}
   notValidRows = {}
   i = 0
   data_list = [['Non Profit', 'Total Amount', 'Total Fee', 'No of donations']]     
   for row in target_doc:
      if(i > 0) :
        isValidValue, reason = isValid(row, supportedCurrencies)
        if(isValidValue):
          if row[2] in resultRow: 
            resultRow[row[2]] = processRow(row, resultRow[row[2]], data['rates'], baseCurrency)
          else:
            resultRow[row[2]] = processRow(row, None, data['rates'], baseCurrency)  
        else:
          notValidRows[i] = reason
      i = i + 1 
   for key in resultRow:
      data_list.append(resultRow[key])
   with open('result.csv', 'w') as resultFile:
      writer = csv.writer(resultFile, delimiter='|')
      writer.writerows(data_list)
   not_valid_data_list = [['Row number', 'Reason']]
   for key in notValidRows:
      not_valid_data_list.append([key, notValidRows[key]])
   with open('not_valid.csv', 'w') as notValidfile:
      writer = csv.writer(notValidfile, delimiter='|')
      writer.writerows(not_valid_data_list)         
def isValid(row, supportedCurrencies):
  if(len(row) != 6):
    return False, "Row length is not 6"
  try:  
        d,m,y = row[0].split('/')
        datetime.datetime(int(y),  
                          int(m), int(d))
  except ValueError:
        return False, "Not correct date format"
  if(row[4].isdigit()):
         return False, "Amount is not a number"
  if(row[4].isdigit()):
         return False, "Fee is not a number"
  if(row[3] not in supportedCurrencies):
        return False, "Currency not supported"
  return True, "True"      


def processRow(row, result, rates, baseCurrency):             
  if(result is None):
    amount = float(row[4]) * rates[baseCurrency]
    feeAmount = float(row[5]) * rates[baseCurrency]
    resultRow = [row[2], amount, feeAmount, 1]
    return resultRow
  else:
    amount = float(row[4]) * rates[baseCurrency] + result[1]
    feeAmount = float(row[5]) * rates[baseCurrency]  + result[2]
    count = 1 + result[3]
    resultRow = [row[2], amount, feeAmount, count]
    return resultRow