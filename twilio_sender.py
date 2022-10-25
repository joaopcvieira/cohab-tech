# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import dotenv_values

envvar = dotenv_values('./.env')


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = envvar['TWILIO_ACCOUNT_SID']
auth_token = envvar['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def send_message(text: str, cel: str) -> None:
    message = client.messages.create(
                              body=text,
                              from_='whatsapp:+14155238886',
                              to=f'whatsapp:+{cel}'
                          )
    print(message.sid)
