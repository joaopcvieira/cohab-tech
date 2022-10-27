# %%
import gspread
import pandas as pd
import re

sa = gspread.service_account(filename='credentials.json')
# sh = sa.open("Home Broker")
# ws = sh.worksheet("nomes")

nomes_cohab = pd.DataFrame(
    sa.open(
        "H8 - 2022.1"
    ).worksheet(
        "H8"
    ).get("A2:F"),

    columns=[
        'bloco_cohab',
        'apto_cohab',
        'vaga_cohab',
        'nome_cohab',
        'apelido_cohab',
        'turma_cohab'
    ]).dropna(subset=['turma_cohab']).fillna('-empty-')

nomes_financeiro = pd.DataFrame(
    sa.open(
        "Cópia de Controle Mensalidade - Base de dados"
    ).worksheet(
        "Import_Range_Planilha_Financeiro_Casd"
    ).get("M5:Q"),

    columns=[
        'cpf_financeiro',
        'nome_financeiro',
        'turma_financeiro',
        'email_financeiro',
        'apelido_financeiro'
    ]).dropna(subset=['nome_financeiro']).fillna('-empty-')


# %%
def remove_accents_and_special_characters(word):
    word = word.lower().strip(' ')
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

def fix_cpf(cpf):
    cpf = str(cpf)
    cpf = cpf.replace('.', '').replace('-', '').replace(' ', '')
    if(len(cpf) == 11):
        return cpf
    elif(len(cpf) == 10):
        return '0' + cpf
    else:
        return "ERRO CPF INVALIDO"



nomes_cohab['nome_cohab'] = nomes_cohab.nome_cohab.apply(remove_accents_and_special_characters).sort_values()
nomes_financeiro['nome_financeiro'] = nomes_financeiro.nome_financeiro.apply(remove_accents_and_special_characters)
nomes_financeiro['cpf_financeiro'] = nomes_financeiro.cpf_financeiro.apply(fix_cpf)

# %%
qtd_nomes_diferentes = 0
for idx, linha in nomes_cohab.iterrows():
    if linha.nome_cohab not in nomes_financeiro.nome_financeiro.values:
        # print(linha.nome_cohab)
        qtd_nomes_diferentes += 1

print(qtd_nomes_diferentes)

# %%
from fuzzywuzzy import process

nome_financeiro_achado = list()
cpf_finaceiro_achado = list()
apelido_financeiro_achado = list()
turma_financeiro_achado = list()
ratio = list()

for idx, linha in nomes_cohab.iterrows():
    if linha.nome_cohab in nomes_financeiro.nome_financeiro.values:
        nome_financeiro_achado.append("")
        cpf_finaceiro_achado.append(
            nomes_financeiro.loc[nomes_financeiro.nome_financeiro == linha.nome_cohab, 'cpf_financeiro'].values[0])
        apelido_financeiro_achado.append("")
        turma_financeiro_achado.append("")
        ratio.append(100)
    else:
        nome_achado = process.extractOne(
            linha.nome_cohab, nomes_financeiro.nome_financeiro.values)
        ratio.append(nome_achado[1])
        [cpf_achado,
         nome_achado,
         turma_achado,
         email_achado,
         apelido_achado
         ] = nomes_financeiro.loc[
            nomes_financeiro.nome_financeiro ==
            nome_achado[0]].values[0]

        nome_financeiro_achado.append(nome_achado)
        cpf_finaceiro_achado.append(cpf_achado)
        apelido_financeiro_achado.append(apelido_achado)
        turma_financeiro_achado.append(turma_achado)

nomes_cohab['nome_financeiro'] = nome_financeiro_achado
nomes_cohab['cpf_financeiro'] = cpf_finaceiro_achado
nomes_cohab['apelido_financeiro'] = apelido_financeiro_achado
nomes_cohab['turma_financeiro'] = turma_financeiro_achado
nomes_cohab['ratio'] = ratio


# %%
# send df to google sheets
sa.open("Nomes Cohab X Financeiro").worksheet("nomes").update([nomes_cohab.columns.values.tolist()] + nomes_cohab.values.tolist())

# %%



