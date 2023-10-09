import requests
#weather
API_KEY = "SECRET"
WS_URL = "http://api.weatherstack.com/current"

cities = []
with open("cities.txt") as f:
    for line in f:
        cities.append(line.strip())
print(cities)

for city in cities:
    parameters = {'access_key': API_KEY, 'query': city}
    response = requests.get(WS_URL, parameters)
    js = response.json()

    temperature = js['current']['temperature']
    date = js['location']['localtime']

    with open(f"{city}.csv", "a") as f:
        f.write(f"{date},{temperature}\n")


#market watch

api = 'SECRET'
url = f'http://api.marketstack.com/v1/eod'

stocks = []
with open('stocks.txt') as s:
  for line in s:
    stocks.append(line.strip())
print(stocks)
for stock in stocks:
  
  parameter = {'access_key': api, 'symbols': stock}
  response = requests.get(url,parameter)
  js = response.json()

  high = js['data'][0]['high']
  low = js['data'][0]['low']
  date = js['data'][0]['date']
  with open(f'{stock}.csv', 'a') as x:
    x.write(f'{date},{high}, {low}\n')
    

  
