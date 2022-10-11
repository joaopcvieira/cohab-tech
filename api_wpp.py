from distutils import text_file
import requests
import pandas as pd
from dotenv import dotenv_values
import urllib

envvar = dotenv_values('./.env')


TOKEN = envvar['TOKEN']
ID_TEL_NUMBER = envvar['ID_TEL_NUMBER']
VERSION = envvar['VERSION']

url_post = f'https://graph.facebook.com/{VERSION}/{ID_TEL_NUMBER}/messages?access_token={TOKEN}'


def send_message(text: str, cel: str) -> None:
    data = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": f"{cel}",
      "type": "text",
      "text": { 
        "preview_url": True,
        "body": text
        }
    }
    try:
        response = requests.post(url_post, json=data, headers={'Content-Type': 'application/json'})
        # print(response.json())
    except Exception as e:
        print(e)

# send_message('''Teste de mnsg
# Multi Linhas *bold*

# asd
# ''', '5561999460906')