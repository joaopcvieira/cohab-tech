import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'joaopcvieira962+sendinblue@gmail.com'
PASSWORD = 'IMRVjrUzXTva4Ggk'


def generate_MIMEText_msg(email: str, containt: str) -> str:
    msg = MIMEMultipart()       # create a message
    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Processo de Postulação Casd 2022"

    # add in the message body
    msg.attach(MIMEText(containt, 'html'))
    return msg


def send_email(email: str, containt: str):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-relay.sendinblue.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # send the message via the server set up earlier.
    s.send_message(generate_MIMEText_msg(email, containt))

    # Terminate the SMTP session and close the connection
    s.quit()
