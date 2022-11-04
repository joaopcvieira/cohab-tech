import gspread
import pandas as pd
import re
from fuzzywuzzy import process
import aux_funcs as aux

sa = gspread.service_account(filename='credentials.json')

# acessa os nomes na planilha atual da cohab
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

# acessa os nomes na planilha atual do financeiro
nomes_financeiro = pd.DataFrame(
    sa.open(
        "Cópia de Controle Mensalidade - Base de dados"
    ).worksheet(
        "export_python"
    ).get("A2:E"),

    columns=[
        'nome_financeiro',
        'turma_financeiro',
        'email_financeiro',
        'apelido_financeiro',
        'cpf_financeiro'
    ]).dropna(subset=['nome_financeiro']).fillna('-empty-')


# Removing accents and special characters from the names and cpf's.
nomes_cohab['nome_cohab'] = nomes_cohab.nome_cohab.apply(
    aux.remove_accents_and_special_characters).sort_values()
nomes_financeiro['nome_financeiro'] = nomes_financeiro.nome_financeiro.apply(
    aux.remove_accents_and_special_characters)
nomes_financeiro['cpf_financeiro'] = nomes_financeiro.cpf_financeiro.apply(
    aux.fix_cpf)


nome_financeiro_achado = list()
cpf_finaceiro_achado = list()
apelido_financeiro_achado = list()
turma_financeiro_achado = list()
ratio = list()

# Iterating over the rows of the dataframe `nomes_cohab` and checking if the name of the row is in the
# `nomes_financeiro` dataframe. If it is, it appends the name, cpf, nickname, and class to the lists
# `nome_financeiro_achado`, `cpf_finaceiro_achado`, `apelido_financeiro_achado`, and
# `turma_financeiro_achado`, respectively. If it is not, it uses the `process.extractOne` function to
# find the closest match and then appends the name, cpf, nickname, and class to the lists
# `nome_financeiro_achado`, `cpf_finaceiro_achado`, `apelido_financeiro_achado`, and
# `turma_financeiro_achado`, respectively.
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
        [nome_achado,
            turma_achado,
            email_achado,
            apelido_achado,
            cpf_achado
         ] = nomes_financeiro.loc[
            nomes_financeiro.nome_financeiro ==
            nome_achado[0]].values[0]

        nome_financeiro_achado.append(nome_achado)
        cpf_finaceiro_achado.append(cpf_achado)
        apelido_financeiro_achado.append(apelido_achado)
        turma_financeiro_achado.append(turma_achado)

# Adding the columns `nome_financeiro`, `cpf_financeiro`, `apelido_financeiro`, `turma_financeiro`,
# and `ratio` to the dataframe `nomes_cohab`.
nomes_cohab['nome_financeiro'] = nome_financeiro_achado
nomes_cohab['cpf_financeiro'] = cpf_finaceiro_achado
nomes_cohab['apelido_financeiro'] = apelido_financeiro_achado
nomes_cohab['turma_financeiro'] = turma_financeiro_achado
nomes_cohab['ratio'] = ratio


# send df to google sheets
status = sa.open("Nomes Cohab X Financeiro").worksheet("nomes").update(
    [nomes_cohab.columns.values.tolist()] + nomes_cohab.values.tolist())
print(status)