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

def get_students_info() -> pd.DataFrame:
    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("Home Broker")
    ws = sh.worksheet("alunos")

    planilha_AG = sa.open('Presença na AG').worksheet("Geral")

    atributos = ['nome',
                'apelido',
                'turma',
                'cpf',
                'email',
                'ap_bloco', 'ap_numero', 'ap_vaga',
                'pontos_total', 'pontos_antigos', 'pontos_presenca', 'pontos_boletos',
                'pontos_iniciativas_I1_nome', 'pontos_iniciativas_I1_pontos',
                'pontos_iniciativas_I2_nome', 'pontos_iniciativas_I2_pontos',
                'pontos_iniciativas_I3_nome', 'pontos_iniciativas_I3_pontos',
                ]
    alunos = pd.DataFrame(columns=atributos, data=ws.get("A2:R"))
    
   
    nomes_alunos_presentes = alunos_presentes_nas_ags().nome.apply(remove_accents_and_special_characters).values
    alunos['pontos_presenca'] = [1 if nome in nomes_alunos_presentes else 0 for nome in alunos.nome.apply(remove_accents_and_special_characters).values]

    alunos_devendo_boletos = boletos_infos().nome.apply(remove_accents_and_special_characters).values
    alunos['devendo_boletos'] = [devendo if nome in alunos_devendo_boletos else '' for devendo, nome in zip(boletos_infos().meses_devendo.values, alunos.nome.apply(remove_accents_and_special_characters).values)]
    # print(alunos.head())

    alunos['pontos_boletos'] = [0.5 if devendo == '' else 0 for devendo in alunos.devendo_boletos.values]


    pontos_total = []
    for idx, linha in alunos.iterrows():
        pt = 2
        print(linha.nome)
        if linha.pontos_antigos != '': # or linha.pontos_antigos.notnull():
            pt += float(linha.pontos_antigos)
        if linha.pontos_boletos != '': # or linha.pontos_boletos.notnull():
            pt += float(linha.pontos_boletos)
        if linha.pontos_presenca != '': # or linha.pontos_presenca.notnull():
            pt += float(linha.pontos_presenca)
        if linha.pontos_iniciativas_I1_pontos != '': # or linha.pontos_iniciativas_I1_pontos.notnull():
            pt += float(linha.pontos_iniciativas_I1_pontos)
        if linha.pontos_iniciativas_I2_pontos != '': # or linha.pontos_iniciativas_I2_pontos.notnull():
            pt += float(linha.pontos_iniciativas_I2_pontos)
        if linha.pontos_iniciativas_I3_pontos != '': # or linha.pontos_iniciativas_I3_pontos.notnull():
            pt += float(linha.pontos_iniciativas_I3_pontos)

        pontos_total.append(pt)
    
    alunos['pontos_total'] = pontos_total
    return alunos

print(get_students_info().head(10))



