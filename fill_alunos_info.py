import pandas as pd
import gspread
import re
from templates import *
from presenca_ag import alunos_presentes_nas_ags
from boletos_infos import boletos_infos
import aux_funcs as aux
from datetime import datetime, date

CURRENT_YEAR = datetime.now().year
TURMA_DE_BIXOS = int(str(CURRENT_YEAR + 4)[2:])  # em 2022 os bixos eram a T26
PONTUACAO_BOLETOS = 0
PONTUACAO_AG = 0.25

sa = gspread.service_account(filename='credentials.json')
sh = sa.open("Alunos db")
ws = sh.worksheet("H8 2022")


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

planilha_AG = sa.open('Presença na AG').worksheet("Geral")

atributos = ['nome', 'apelido', 'turma', 'cpf',
                'celular', 'email',
                'ap_bloco', 'ap_numero', 'ap_vaga',
                'pontos_total', 'pontos_antigos', 'pontos_presenca', 'pontos_boletos',
                'pontos_iniciativas_I1_nome', 'pontos_iniciativas_I1_pontos',
                'pontos_iniciativas_I2_nome', 'pontos_iniciativas_I2_pontos',
                'pontos_iniciativas_I3_nome', 'pontos_iniciativas_I3_pontos',
                'pontos_extra'
                ]
alunos = pd.DataFrame(columns=atributos, data=ws.get("A3:U"))

# pegando as pontuações antigas
ws_2021 = sa.open(
    "Validação de Pontos - Cohab (respostas)").worksheet("Pontos 2.0")
df_pontos_anteriores = pd.DataFrame(columns=ws_2021.get("A1:AH1")[
                                    0], data=ws_2021.get("A2:AH"))

df_pontos_anteriores = df_pontos_anteriores[['Nome', 'CPF', 'Total']]
df_pontos_anteriores.rename(
    columns={'Nome': 'nome', 'CPF':'cpf', 'Total': 'pontos_antigos'}, inplace=True)
# df_pontos_anteriores['nome_join'] = df_pontos_anteriores['nome'].apply(
#     aux.remove_accents_and_special_characters)
    
df_pontos_anteriores.pontos_antigos = df_pontos_anteriores.pontos_antigos.apply(aux.fix_number).astype(float)
df_pontos_anteriores.cpf = df_pontos_anteriores.cpf.apply(aux.fix_cpf).astype(str)

# Analisando os pontos de presença
nomes_alunos_presentes = alunos_presentes_nas_ags().nome.apply(
    aux.remove_accents_and_special_characters).values
alunos['pontos_presenca'] = [PONTUACAO_AG if nome in nomes_alunos_presentes else
                                0 for nome in alunos.nome.apply(
                                    aux.remove_accents_and_special_characters).values]


# Analisando os pontos de boletos
boletos_df = boletos_infos()
# Criando uma coluna temporária para a junção dos df
boletos_df['nome_join'] = boletos_df.nome.apply(
    aux.remove_accents_and_special_characters)
alunos['nome_join'] = alunos.nome.apply(
    aux.remove_accents_and_special_characters)
alunos['cpf'] = alunos.cpf.apply(aux.fix_cpf).astype(str)
df_pontos_anteriores['cpf'] = df_pontos_anteriores.cpf.apply(aux.fix_cpf).astype(str)

alunos = pd.merge(
    alunos, boletos_df[['nome_join', 'meses_devendo']], on='nome_join', how='left')
    
# alunos = pd.merge(alunos, df_pontos_anteriores, on='cpf', how='outer')

nomes_pontuacao_anterior = df_pontos_anteriores['nome'].values
cpf_pontuacao_anterior = df_pontos_anteriores['cpf'].values
pontos_antigos = list()

for idx, linha in alunos.iterrows():
    if linha.cpf in cpf_pontuacao_anterior:
        pontos_antigos.append(
            df_pontos_anteriores.loc[df_pontos_anteriores.cpf == linha.cpf, 'pontos_antigos'].values[0])
        continue
    
    if linha.cpf in cpf_pontuacao_anterior:
        print("PQP")

    certainty, best_option = aux.is_name_in_list(
        linha.nome, nomes_pontuacao_anterior)

    if certainty:
        pontos_antigos.append(
            df_pontos_anteriores.loc[df_pontos_anteriores.nome == best_option, 'pontos_antigos'].values[0])

    else:
        pontos_antigos.append(0)

alunos['pontos_antigos'] = pontos_antigos
alunos[['nome', 'apelido', 'cpf', 'turma', 'pontos_antigos']]

alunos_esquisitos = df_pontos_anteriores.loc[df_pontos_anteriores.cpf.isin(alunos.cpf.values)]
# alunos_esquisitos
# pd.concat([alunos, alunos_esquisitos])

alunos.append(alunos_esquisitos)

# alunos.loc[alunos.apelido.isna()]

alunos.loc[(alunos.pontos_antigos == 0) &
           (alunos.turma < '26'),
           'pontos_antigos'
           ] = alunos.loc[(alunos.pontos_antigos == 0) &
                          (alunos.turma < '26')].apply(
                            lambda x: 2*(TURMA_DE_BIXOS - int(x.turma)),  axis=1).values

alunos.drop(columns=['nome_join'], inplace=True)

# alunos.nome_x.fillna(alunos.no    me_y, inplace=True)


alunos.rename(columns={
    'nome_x': 'nome',
    'cpf_x': 'cpf',
    'pontos_antigos_y': 'pontos_antigos'
    }, inplace=True)
alunos['pontos_antigos'] = alunos.pontos_antigos.fillna(0)
# alunos['pontos_antigos'] = alunos.pontos_antigos.apply(aux.fix_number)

alunos = alunos[[
    'nome', 'apelido', 'turma', 'cpf', 'celular', 'email',
    'ap_bloco', 'ap_numero', 'ap_vaga',
    'pontos_total', 'pontos_antigos', 'pontos_presenca', 'pontos_boletos',
    'pontos_iniciativas_I1_nome', 'pontos_iniciativas_I1_pontos',
    'pontos_iniciativas_I2_nome', 'pontos_iniciativas_I2_pontos',
    'pontos_iniciativas_I3_nome', 'pontos_iniciativas_I3_pontos',
    'pontos_extra', 'meses_devendo'
]]

alunos = alunos.fillna('-')



alunos['pontos_presenca'] = alunos['pontos_presenca'].apply(fix_number)
alunos['pontos_iniciativas_I1_pontos'] = alunos['pontos_iniciativas_I1_pontos'].apply(fix_number)
alunos['pontos_iniciativas_I2_pontos'] = alunos['pontos_iniciativas_I2_pontos'].apply(fix_number)
alunos['pontos_iniciativas_I3_pontos'] = alunos['pontos_iniciativas_I3_pontos'].apply(fix_number)
alunos['pontos_extra'] = alunos['pontos_extra'].apply(fix_number)

alunos['pontos_boletos'] = [PONTUACAO_BOLETOS if devendo ==
                            '-' else 0 for devendo in alunos.meses_devendo.values]

alunos['pontos_total'] = get_pontos_total(alunos)

ws_export = sh.worksheet("H8 + info boletos")

i = 2
ws_export.clear()
ws_export.update('A1', 'Banco de Dados de Alunos + info boletos - H8 2022 - atualizado em ' +
                    datetime.strftime(datetime.now(), "%d/%m/%Y"))
ws_export.update(f"A{i}:U", [
    alunos.columns.values.tolist()] + alunos.values.tolist())
