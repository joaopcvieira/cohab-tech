import pandas as pd
import gspread
# from templates import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

sa = gspread.service_account(filename='credentials.json')
sh = sa.open("Home Broker")
ws = sh.worksheet("alunos")

print(ws.get("A1:K1")[0])


atributos = ['nome',
             'apelido',
             'turma',
             'cpf',
             'email',
             'ap-bloco', 'ap-numero', 'ap-vaga',
             'pontos-total', 'pontos-presenca', 'pontos-boletos',
             'pontos-iniciativas-I1-nome', 'pontos-iniciativas-I1-pontos',
             'pontos-iniciativas-I2-nome', 'pontos-iniciativas-I2-pontos',
             'pontos-iniciativas-I3-nome', 'pontos-iniciativas-I3-pontos',
             ]
alunos = pd.DataFrame(columns=atributos, data=ws.get("A2:Q100"))

print(alunos.head())


# for index, aluno in alunos.iterrows():
#     print(aluno['nome'])
#     print(aluno['email'])
#     print(aluno['pontos-total'])
#     print(aluno['pontos-presenca'])
#     print(aluno['pontos-boletos'])
#     print(aluno['pontos-iniciativas-I1-nome'])
#     print(aluno['pontos-iniciativas-I1-pontos'])
#     print(aluno['pontos-iniciativas-I2-nome'])
#     print(aluno['pontos-iniciativas-I2-pontos'])
#     print(aluno['pontos-iniciativas-I3-nome'])
#     print(aluno['pontos-iniciativas-I3-pontos'])
#     print()
