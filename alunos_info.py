import pandas as pd
import gspread
import re
from templates import *
from presenca_ag import alunos_presentes_nas_ags
from boletos_infos import boletos_infos

def remove_accents_and_special_characters(word):
    word = word.lower()
    word = re.sub(pattern=r'[àáâãäå]', repl='a', string=word)
    word = re.sub(pattern=r'[èéêë]', repl='e', string=word)
    word = re.sub(pattern=r'[ìíîï]', repl='i', string=word)
    word = re.sub(pattern=r'[òóôõö]', repl='o', string=word)
    word = re.sub(pattern=r'[ùúûü]', repl='u', string=word)
    word = re.sub(
        # Remove anything that is not a word or digit
        pattern=r'[^a-zA-Z0-9\s]', repl='', string=word
    )
    return word

def get_pontos_total(alunos: pd.DataFrame) -> pd.DataFrame:
    pontos_total = []
    for idx, linha in alunos.iterrows():
        pt = 2
        try:
            pt += float(linha.pontos_antigos)
        except:
            pass
        try:
            pt += float(linha.pontos_boletos)
        except:
            pass
        try:
            pt += float(linha.pontos_presenca)
        except:
            pass
        try:
            pt += float(linha.pontos_iniciativas_I1_pontos)
        except:
            pass
        try:
            pt += float(linha.pontos_iniciativas_I2_pontos)
        except:
            pass
        try:
            pt += float(linha.pontos_iniciativas_I3_pontos)
        except:
            pass

        pontos_total.append(pt)
    return pontos_total


def get_students_info() -> pd.DataFrame:
    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("Home Broker")
    ws = sh.worksheet("alunos")

    planilha_AG = sa.open('Presença na AG').worksheet("Geral")

    atributos = ['nome',
                 'apelido',
                 'turma',
                 'cpf',
                 'celular', 'email',
                 'ap_bloco', 'ap_numero', 'ap_vaga',
                 'pontos_total', 'pontos_antigos', 'pontos_presenca', 'pontos_boletos',
                 'pontos_iniciativas_I1_nome', 'pontos_iniciativas_I1_pontos',
                 'pontos_iniciativas_I2_nome', 'pontos_iniciativas_I2_pontos',
                 'pontos_iniciativas_I3_nome', 'pontos_iniciativas_I3_pontos',
                 ]
    alunos = pd.DataFrame(columns=atributos, data=ws.get("A2:S"))

    # Analisando os pontos de presença
    nomes_alunos_presentes = alunos_presentes_nas_ags().nome.apply(
        remove_accents_and_special_characters).values
    alunos['pontos_presenca'] = [1 if nome in nomes_alunos_presentes else
                                 0 for nome in alunos.nome.apply(
                                     remove_accents_and_special_characters).values]

    # Analisando os pontos de boletos
    boletos_df = boletos_infos()
    # Criando uma coluna temporária para a junção dos df
    boletos_df['nome_join'] = boletos_df.nome.apply(
        remove_accents_and_special_characters)
    alunos['nome_join'] = alunos.nome.apply(
        remove_accents_and_special_characters)

    alunos = pd.merge(
        alunos, boletos_df[['nome_join', 'meses_devendo']], on='nome_join', how='left')
    alunos.drop(columns=['nome_join'], inplace=True)

    alunos = alunos.fillna('-')
    alunos['pontos_boletos'] = [0.5 if devendo == '-' else 0 for devendo in alunos.meses_devendo.values]

    alunos['pontos_total'] = get_pontos_total(alunos)

    ws_export = sh.worksheet("import_python")
    ws_export.update([alunos.columns.values.tolist()] + alunos.values.tolist())
    return alunos

# df = get_students_info()
# print(df)
