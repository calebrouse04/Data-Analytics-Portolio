import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import http.client
import json
import pandas as pd

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 5TGNFOiXwuBcTXKvwtqVE1:2kvBr4BjBeCyMd7vr4BXIj"
}

conn.request("GET", "/gasPrice/stateUsaPrice?state=TN", headers=headers)

res = conn.getresponse()
data = res.read()

data_dict = json.loads(data.decode("utf-8"))  # convert bytes to dict

# Check if the request was successful
if data_dict['success']:
    result = data_dict['result']
    
    # Convert the 'state' dictionary to a DataFrame and display it
    state_df = pd.DataFrame([result['state']])
    print("State Data:\n", state_df)
    state_df.to_excel('StateData.xlsx')
    
    # Convert the 'cities' list (of dictionaries) to a DataFrame and display it
    cities_df = pd.DataFrame(result['cities'])
    print("\nCities Data:\n", cities_df)
    cities_df.to_excel('CitiesData.xlsx')

mail_content = ''

# setup the addresses and start the MIME
mail_sender = 'calebrouse11@gmail.com'
mail_receiver = 'calebrouse11@gmail.com'
password = 'mbjipwjoexvxtvxq' # enter your email password

msg = MIMEMultipart()
msg['From'] = mail_sender
msg['To'] = mail_receiver
msg['Subject'] = 'Fuel Prices Data'

# add in the message body
msg.attach(MIMEText(mail_content, 'plain'))

# attach the dataframe data
html1 = state_df.to_html()
html2 = cities_df.to_html()

# Attach HTML. add 2 parts to MIMEMultipart message
# The MIMEText objects with 'html' parameter.
msg.attach(MIMEText(html1, 'html'))
msg.attach(MIMEText(html2, 'html'))

# create server
server = smtplib.SMTP('smtp.gmail.com: 587')

server.starttls()

# Login Credentials for sending the mail
server.login(msg['From'], password)

# send the message via the server
server.sendmail(msg['From'], msg['To'], msg.as_string())

server.quit()

print("Successfully sent email to %s:" % (msg['To']))

time.sleep(60 * 60 *24)
