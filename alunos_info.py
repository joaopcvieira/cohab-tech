import pandas as pd
import gspread
import re
from templates import *
from presenca_ag import alunos_presentes_nas_ags
from boletos_infos import boletos_infos
import aux_funcs as aux
from datetime import datetime, date
import numpy as np


PONTUACAO_BOLETOS = 0
PONTUACAO_AG = 0.25


def fix_number(num):
    try:
        return float(num)
    except:
        return aux.fix_number(num)


def get_pontos_total(alunos: pd.DataFrame):
    pontos_total = []

    for idx, linha in alunos.iterrows():
        pt = 2
        try:
            pt += fix_number(linha.pontos_antigos)
        except:
            pass
        try:
            pt += fix_number(linha.pontos_boletos)
        except:
            pass
        try:
            pt += fix_number(linha.pontos_presenca)
        except:
            pass
        try:
            pt += fix_number(linha.pontos_iniciativas_I1_pontos)
        except:
            pass
        try:
            pt += fix_number(linha.pontos_iniciativas_I2_pontos)
        except:
            pass
        try:
            pt += fix_number(linha.pontos_iniciativas_I3_pontos)
        except:
            pass
        try:
            pt += fix_number(linha.pontos_extra)
        except:
            pass

        pontos_total.append(pt)
    return pontos_total


def get_students_info() -> pd.DataFrame:
    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("Alunos db")
    ws = sh.worksheet("H8 + info boletos")


    alunos = pd.DataFrame(ws.get("A3:U"), columns=ws.get("A2:U2")[
                        0]).dropna(subset=['nome'])
    return alunos

# df = get_students_info()
# print(df)


def update_mnsg_sheets_manual_check(mensagens: np.array):
    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("Alunos db")
    ws = sh.worksheet("manual_check")

    ws.update('V3', mensagens.transpose().tolist())

    null_arr = np.array([['' for x in range(1000)]])
    ws.update('X3', null_arr.transpose().tolist())
    return


def update_mnsg_sheets_2022_forms(mensagens: np.array):
    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("Alunos db")
    ws = sh.worksheet("2022_forms")

    ws.update('N2', mensagens.transpose().tolist())
    return
