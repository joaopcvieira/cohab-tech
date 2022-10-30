import pandas as pd
import gspread
import aux_funcs as aux
import numpy as np

sa = gspread.service_account(filename='credentials.json')

sh = sa.open('H8 - 2022.1')

pl_cohab = sh.worksheet('H8')

# Get data from CoHab
pl_cohab = sa.open('H8 - 2022.1').worksheet('H8')

df_cohab = pd.DataFrame(pl_cohab.get("A2:F"),
                        columns=['ap_bloco', 'ap_numero', 'ap_vaga',
                                 'nome', 'apelido', 'turma'
                                 ])

df_cohab.turma = df_cohab.turma.apply(lambda x: x[2:] if x else '')
df_cohab.ap_bloco = df_cohab.ap_bloco.apply(lambda x: x[3:] if x else '')
df_cohab = df_cohab.loc[df_cohab.turma.notna()]
df_cohab = df_cohab.loc[df_cohab.turma != ""]


# Get data from Financeiro
pl_financeiro = sa.open('Controle Mensalidade - Base de dados').worksheet('H8')
pl_financeiro.get("A4:Q4")
df_financeiro = pd.DataFrame(columns=pl_financeiro.get("A4:Q4")[0],
                             data=pl_financeiro.get("A5:Q"))
df_financeiro.rename(columns={
    'NOME': 'nome',
    'Apelido': 'apelido',
    'T': 'turma',
    'EMAIL1': 'email',
    'Meses': 'meses_devendo',
    'ALOJ': 'ap_bloco',
    'APTO': 'ap_numero',
    'VAGA': 'ap_vaga',
    'CPF': 'cpf',
    'CELULAR': 'celular',
    'STATUS': 'status'
}, inplace=True)

df_financeiro.turma = df_financeiro.turma.apply(lambda x: x[2:] if x else '')
df_financeiro.ap_bloco = df_financeiro.ap_bloco.apply(
    lambda x: x[3:] if x else '')
df_financeiro.celular = df_financeiro.celular.apply(aux.fix_cel)
df_financeiro.cpf = df_financeiro.cpf.apply(aux.fix_cpf)

df_financeiro = df_financeiro[[
    'nome', 'apelido', 'turma',
    'cpf', 'celular', 'email',
    'ap_bloco', 'ap_numero', 'ap_vaga',
    'meses_devendo', 'status'
]]

df_financeiro.dropna(subset='nome')
df_financeiro = df_financeiro.loc[df_financeiro.nome.notna()]
df_financeiro = df_financeiro.loc[df_financeiro.turma >= "22"]
df_financeiro.reset_index(drop=True, inplace=True)


# Get data from Controle de Efetivo
pl_controle_efetivo = sa.open(
    "Controle de Efetivo das Iniciativas 2022.2").worksheet('summary_iniciativas')
df_controle_efetivo = pd.DataFrame(columns=pl_controle_efetivo.get("B2:I2")[
                                   0], data=pl_controle_efetivo.get("B3:I"))


df_cohab.fillna('', inplace=True)
df_financeiro.fillna('', inplace=True)
df_controle_efetivo.fillna('', inplace=True)


# Check if aptos in cohab are the same as in financeiro
apto_adress_cohab = 'H8-' + df_cohab['ap_bloco'] + ' apto ' + \
    df_cohab['ap_numero'] + ' vaga ' + df_cohab['ap_vaga']
teste_cohab = pd.DataFrame(columns=['apelido', 'nome', 'turma', 'apto_adress_cohab'], data=zip(
    df_cohab['apelido'],  df_cohab['nome'], df_cohab['turma'], apto_adress_cohab))

temp_fiananceiro = df_financeiro  # .loc[df_financeiro.ap_bloco != '']
apto_adress_financeiro = 'H8-' + temp_fiananceiro['ap_bloco'] + ' apto ' + \
    temp_fiananceiro['ap_numero'] + ' vaga ' + temp_fiananceiro['ap_vaga']
teste_financeiro = pd.DataFrame(columns=['apelido', 'nome', 'turma', 'apto_adress_financeiro', 'statusfinanceiro'], data=zip(
    temp_fiananceiro['apelido'],  temp_fiananceiro['nome'], temp_fiananceiro['turma'], apto_adress_financeiro, temp_fiananceiro['status']))

teste_financeiro.sort_values(by='apto_adress_financeiro', inplace=True)
teste_cohab.sort_values(by='apto_adress_cohab', inplace=True)

df = pd.merge(teste_cohab, teste_financeiro, how='outer', left_on=[
              'apto_adress_cohab'], right_on=['apto_adress_financeiro'], suffixes=('_cohab', '_financeiro'))


certo = []
retios_name = []
retios_apelido = []
for idx, linha in df.iterrows():
    equivalent_name, ratio_name = aux.is_name_equivalent(
        f'{ linha.nome_cohab }', f'{linha.nome_financeiro}')
    equivalent_apelido, ratio_apelido = aux.is_name_equivalent(
        f'{linha.apelido_cohab}', f'{linha.apelido_financeiro}')
    if equivalent_name or equivalent_apelido:
        certo.append(True)
    else:
        certo.append(False)

    retios_name.append(ratio_name)
    retios_apelido.append(ratio_apelido)

df['check'] = certo
df['ratio_name'] = retios_name
df['ratio_apelido'] = retios_apelido
# df.loc[df.check == False]

# Check alunos that signed TVR and are in cohab
df_TVR = df_financeiro.loc[df_financeiro.status.str.contains('TVR')]
df_TVR

filter = []
status = []
nomes_TVR = df_TVR.nome.values
for idx, linha in df_cohab.iterrows():
    is_name, name = aux.is_name_in_list(f'{linha.nome}', nomes_TVR)
    if is_name:
        # print(f'{linha.apelido} - {linha.nome} - {linha.turma} - {linha.ap_bloco} - {linha.ap_numero} - {linha.ap_vaga}')
        filter.append(True)
        status.append(df_TVR.loc[df_TVR.nome == name].status.values[0])
    else:
        filter.append(False)

df_TVR = df_cohab.loc[filter]
df_TVR['status'] = status


# Check alunos that signed TVR and are in cohab
apto_adress_cohab = 'H8-' + df_cohab['ap_bloco'] + ' apto ' + \
    df_cohab['ap_numero'] + ' vaga ' + df_cohab['ap_vaga']
# teste_cohab = pd.DataFrame(columns=['apelido', 'nome', 'turma', 'apto_adress_cohab'], data=zip(df_cohab['apelido'],  df_cohab['nome'], df_cohab['turma'], apto_adress_cohab))
df_cohab['apto_adress_cohab'] = apto_adress_cohab


temp_fiananceiro = df_financeiro.loc[df_financeiro.ap_bloco != '']
apto_adress_financeiro = 'H8-' + temp_fiananceiro['ap_bloco'] + ' apto ' + \
    temp_fiananceiro['ap_numero'] + ' vaga ' + temp_fiananceiro['ap_vaga']
# teste_financeiro = pd.DataFrame(columns=['apelido', 'nome', 'turma', 'apto_adress_financeiro', 'status_financeiro'], data=zip(temp_fiananceiro['apelido'],  temp_fiananceiro['nome'], temp_fiananceiro['turma'], apto_adress_financeiro, temp_fiananceiro['status']))

df_financeiro['apto_adress_financeiro'] = apto_adress_financeiro

df_financeiro.sort_values(by='apto_adress_financeiro', inplace=True)
df_cohab.sort_values(by='apto_adress_cohab', inplace=True)

df_fin_e_cohab = pd.merge(df_cohab, df_financeiro, how='outer', left_on=[
                          'apto_adress_cohab'], right_on=['apto_adress_financeiro'], suffixes=('_cohab', '_financeiro'))
df_fin_e_cohab.dropna(subset=['apto_adress_cohab'], inplace=True)
df_fin_e_cohab


ratios_name = []
ratios_apelido = []
nomes_iniciativas = df_controle_efetivo.nome.values
apelidos_iniciativas = df_controle_efetivo.apelido.values

nome_iniciativas = list()
apelido_iniciativas = list()
pontos_iniciativas_I1_nome = list()
pontos_iniciativas_I1_pontos = list()
pontos_iniciativas_I2_nome = list()
pontos_iniciativas_I2_pontos = list()
pontos_iniciativas_I3_nome = list()
pontos_iniciativas_I3_pontos = list()

for idx, linha in df_fin_e_cohab.iterrows():
    is_equivalent_name, equivalent_name = aux.is_name_in_list(
        f'{ linha.nome_cohab }', nomes_iniciativas)

    is_equivalent_apelido, equivalent_apelido = aux.is_name_in_list(
        f'{linha.apelido_cohab}', apelidos_iniciativas)

    if is_equivalent_name:
        pontos_iniciativas_I1_nome.append(
            df_controle_efetivo.loc[df_controle_efetivo.nome == equivalent_name].pontos_iniciativas_I1_nome.values[0])
        pontos_iniciativas_I1_pontos.append(
            df_controle_efetivo.loc[df_controle_efetivo.nome == equivalent_name].pontos_iniciativas_I1_pontos.values[0])
        pontos_iniciativas_I2_nome.append(
            df_controle_efetivo.loc[df_controle_efetivo.nome == equivalent_name].pontos_iniciativas_I2_nome.values[0])
        pontos_iniciativas_I2_pontos.append(
            df_controle_efetivo.loc[df_controle_efetivo.nome == equivalent_name].pontos_iniciativas_I2_pontos.values[0])
        pontos_iniciativas_I3_nome.append(
            df_controle_efetivo.loc[df_controle_efetivo.nome == equivalent_name].pontos_iniciativas_I3_nome.values[0])
        pontos_iniciativas_I3_pontos.append(
            df_controle_efetivo.loc[df_controle_efetivo.nome == equivalent_name].pontos_iniciativas_I3_pontos.values[0])

    elif is_equivalent_apelido:
        pontos_iniciativas_I1_nome.append(
            df_controle_efetivo.loc[df_controle_efetivo.apelido == equivalent_apelido].pontos_iniciativas_I1_nome.values[0])
        pontos_iniciativas_I1_pontos.append(
            df_controle_efetivo.loc[df_controle_efetivo.apelido == equivalent_apelido].pontos_iniciativas_I1_pontos.values[0])
        pontos_iniciativas_I2_nome.append(
            df_controle_efetivo.loc[df_controle_efetivo.apelido == equivalent_apelido].pontos_iniciativas_I2_nome.values[0])
        pontos_iniciativas_I2_pontos.append(
            df_controle_efetivo.loc[df_controle_efetivo.apelido == equivalent_apelido].pontos_iniciativas_I2_pontos.values[0])
        pontos_iniciativas_I3_nome.append(
            df_controle_efetivo.loc[df_controle_efetivo.apelido == equivalent_apelido].pontos_iniciativas_I3_nome.values[0])
        pontos_iniciativas_I3_pontos.append(
            df_controle_efetivo.loc[df_controle_efetivo.apelido == equivalent_apelido].pontos_iniciativas_I3_pontos.values[0])

    else:
        pontos_iniciativas_I1_nome.append('')
        pontos_iniciativas_I1_pontos.append('')
        pontos_iniciativas_I2_nome.append('')
        pontos_iniciativas_I2_pontos.append('')
        pontos_iniciativas_I3_nome.append('')
        pontos_iniciativas_I3_pontos.append('')

    nome_iniciativas.append(equivalent_name)
    apelido_iniciativas.append(equivalent_apelido)

    # ratios_name.append(ratio_name)
    # ratios_apelido.append(ratio_apelido)

df_fin_cohab_iniciativas = df_fin_e_cohab.copy()
df_fin_cohab_iniciativas['nome_iniciativa'] = nome_iniciativas
df_fin_cohab_iniciativas['apelido_iniciativa'] = apelido_iniciativas
df_fin_cohab_iniciativas['pontos_iniciativas_I1_nome'] = pontos_iniciativas_I1_nome
df_fin_cohab_iniciativas['pontos_iniciativas_I1_pontos'] = pontos_iniciativas_I1_pontos
df_fin_cohab_iniciativas['pontos_iniciativas_I2_nome'] = pontos_iniciativas_I2_nome
df_fin_cohab_iniciativas['pontos_iniciativas_I2_pontos'] = pontos_iniciativas_I2_pontos
df_fin_cohab_iniciativas['pontos_iniciativas_I3_nome'] = pontos_iniciativas_I3_nome
df_fin_cohab_iniciativas['pontos_iniciativas_I3_pontos'] = pontos_iniciativas_I3_pontos

# Creating df_alunos_export
cols_summary = [
    'nome', 'apelido', 'turma', 'cpf', 'celular', 'email',
    'ap_bloco', 'ap_numero', 'ap_vaga',
    'pontos_total', 'pontos_antigos',
    'pontos_presenca', 'pontos_boletos',
    'pontos_iniciativas_I1_nome', 'pontos_iniciativas_I1_pontos',
    'pontos_iniciativas_I2_nome', 'pontos_iniciativas_I2_pontos',
    'pontos_iniciativas_I3_nome', 'pontos_iniciativas_I3_pontos',
    'meses_devendo'
]

df_alunos_export = pd.DataFrame(columns=cols_summary)
df_alunos_export['nome'] = df_fin_cohab_iniciativas['nome_cohab']
df_alunos_export['apelido'] = df_fin_cohab_iniciativas['apelido_cohab']
df_alunos_export['turma'] = df_fin_cohab_iniciativas['turma_cohab']
df_alunos_export['cpf'] = df_fin_cohab_iniciativas['cpf']
df_alunos_export['celular'] = df_fin_cohab_iniciativas['celular']
df_alunos_export['email'] = df_fin_cohab_iniciativas['email']
df_alunos_export['ap_bloco'] = df_fin_cohab_iniciativas['ap_bloco_cohab']
df_alunos_export['ap_numero'] = df_fin_cohab_iniciativas['ap_numero_cohab']
df_alunos_export['ap_vaga'] = df_fin_cohab_iniciativas['ap_vaga_cohab']
# df_alunos_export['pontos_total']
# df_alunos_export['pontos_antigos']
# df_alunos_export['pontos_presenca']
# df_alunos_export['pontos_boletos']
df_alunos_export['pontos_iniciativas_I1_nome'] = df_fin_cohab_iniciativas['pontos_iniciativas_I1_nome']
df_alunos_export['pontos_iniciativas_I1_pontos'] = df_fin_cohab_iniciativas['pontos_iniciativas_I1_pontos']
df_alunos_export['pontos_iniciativas_I2_nome'] = df_fin_cohab_iniciativas['pontos_iniciativas_I2_nome']
df_alunos_export['pontos_iniciativas_I2_pontos'] = df_fin_cohab_iniciativas['pontos_iniciativas_I2_pontos']
df_alunos_export['pontos_iniciativas_I3_nome'] = df_fin_cohab_iniciativas['pontos_iniciativas_I3_nome']
df_alunos_export['pontos_iniciativas_I3_pontos'] = df_fin_cohab_iniciativas['pontos_iniciativas_I3_pontos']
df_alunos_export.head()


df_alunos_export.columns

df_alunos_export.fillna('', inplace=True)
df_alunos_export.sort_values(by=['nome'], inplace=True)

sh = sa.open('Alunos db')
export = sh.worksheet('H8 2022')
export.clear()

i = 2
export.update('A1', 'Banco de Dados de Alunos - H8 2022')
export.update(f"A{i}:S{df_alunos_export.shape[0] + i}", [
              df_alunos_export.columns.values.tolist()] + df_alunos_export.values.tolist())
