import pandas as pd
import gspread
import aux_funcs as aux
import numpy as np

## Pipeline:
# 1) Acessa todas as abas da planilha colocando os nomes das pessoas com a iniciativa e a pontuação
# 2) Se a pessoa já está no dataframe, ela é posta na próxima coluna (proxima iniciativa)
# 3) Se a pessoa está em mais de 3 iniciativas, mantêm-se as 3 maiores apenas


sa = gspread.service_account(filename='credentials.json')
sh = sa.open("Controle de Efetivo das Iniciativas 2022.2")

names = ['CR26', 'AAAITA', 'Aerodesign', 'AGITA',
         'ABU', 'CASD - Curso', 'Carniceria',
         'CEE', 'DepCult', 'eVTOL', 'Formula ITA',
         'ITA Baja', 'ITA Finance', 'ITA Jr', 'ITA Bits',
         'ITA Rocket', 'ITA Androids', 'Rede_', 'ITA Pilots',
         'ITA Robio', 'Casd - Centro']



sum = pd.DataFrame(columns=['nome', 'apelido', 'iniciativa', 'pontuacao'])

for sheet in names:
    ws = sh.worksheet(sheet)
    sheet_df = pd.DataFrame(ws.get("A6:H"), columns=ws.get("A5:H5")[
                            0]).dropna(subset=['Nome'])

    temp_df = pd.DataFrame(
        columns=['nome', 'apelido', 'iniciativa', 'pontuacao'])
    temp_df['nome'] = sheet_df['Nome']
    temp_df['apelido'] = sheet_df['Apelido']
    temp_df['iniciativa'] = str(sheet)
    if sheet == 'CR26':
        temp_df['pontuacao'] = sheet_df['Pontos por 2022'].apply(aux.fix_number)
    else:
        temp_df['pontuacao'] = sheet_df['Pontos por 2022.1'].apply(aux.fix_number) + \
            sheet_df['Pontos extras 2022.1'].apply(aux.fix_number) + \
            sheet_df['Pontos por 2022.2'].apply(aux.fix_number) + \
            sheet_df['Pontos extras 2022.2'].apply(aux.fix_number)

    sum = pd.concat([sum, temp_df], ignore_index=True)


sum.dropna(subset=['pontuacao'], inplace=True)
sum = sum.loc[sum.pontuacao > 0]
sum.sort_values(by=['nome', 'pontuacao'], ascending=False, inplace=True)
sum.reset_index(inplace=True, drop=True)

sum = sum.loc[sum.nome != 'a']


cols_summary = [
    'nome', 'apelido',
    'pontos_iniciativas_I1_nome',
    'pontos_iniciativas_I1_pontos',
    'pontos_iniciativas_I2_nome',
    'pontos_iniciativas_I2_pontos',
    'pontos_iniciativas_I3_nome',
    'pontos_iniciativas_I3_pontos']


df_summary_iniciativas = pd.DataFrame(columns=cols_summary)
df_summary_iniciativas


cols = ['nome', 'apelido', 'turma',
        'cpf', 'celular', 'email',
        'ap_bloco', 'ap_numero', 'ap_vaga',
        'pontos_total', 'pontos_antigos', 'pontos_presenca',
        'pontos_boletos',
        'pontos_iniciativas_I1_nome',
        'pontos_iniciativas_I1_pontos',
        'pontos_iniciativas_I2_nome',
        'pontos_iniciativas_I2_pontos',
        'pontos_iniciativas_I3_nome',
        'pontos_iniciativas_I3_pontos']

df_alunos_final = pd.DataFrame(columns=cols)

sum


not_described_sum = sum.groupby('apelido').agg(
    {'nome': ', '.join, 'iniciativa': ', '.join, 'pontuacao': 'sum'}).sort_values(by='nome', ascending=False)
not_described_sum.reset_index(inplace=True)
not_described_sum.sort_values(by='apelido', ascending=True, inplace=True)


ws = sh.worksheet('not_described')
ws.clear()

i = 2
ws.update('A1', 'Soma de pontos por iniciativa, não descrita por iniciativa')
ws.update(f"B{i}:E{not_described_sum.shape[0] + i}", [
          not_described_sum.columns.values.tolist()] + not_described_sum.values.tolist())


sum = sum.sort_values(by='pontuacao', ascending=False).reset_index(drop=True)

for idx, linha in sum.iterrows():
    df_summary_iniciativas.pontos_iniciativas_I1_pontos.apply(aux.fix_number)
    df_summary_iniciativas.pontos_iniciativas_I2_pontos.apply(aux.fix_number)
    df_summary_iniciativas.pontos_iniciativas_I3_pontos.apply(aux.fix_number)

    if df_summary_iniciativas.shape[0] > 0:
        nomes_ja_inseridos = df_summary_iniciativas['nome'].to_list()
        apelidos_ja_inseridos = df_summary_iniciativas['apelido'].to_list()
        df_summary_iniciativas.pontos_iniciativas_I2_pontos.apply(aux.fix_number)
        df_summary_iniciativas.pontos_iniciativas_I3_pontos.apply
    else:
        nomes_ja_inseridos = ['']
        apelidos_ja_inseridos = ['']

    if aux.is_name_in_list(linha['apelido'], apelidos_ja_inseridos)[0]:
        best_option = aux.is_name_in_list(
            linha['apelido'], apelidos_ja_inseridos)[1]
        # print(best_option)

        if df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option), 'pontos_iniciativas_I3_pontos'].values[0] > 0:
            # check wether the new iniciative has more points than the ones before
            # if so, change it
            pontos = df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option),
                                                ['pontos_iniciativas_I1_pontos', 'pontos_iniciativas_I2_pontos',
                                                    'pontos_iniciativas_I3_pontos']
                                                ].values[0]

            if 0 in pontos or linha.pontuacao > max(pontos):
                i = np.argmin(pontos) + 1
                col = f'pontos_iniciativas_I{i}_'
                df_summary_iniciativas.loc[(
                    df_summary_iniciativas.apelido == best_option), col + 'nome'] = linha.iniciativa
                df_summary_iniciativas.loc[(
                    df_summary_iniciativas.apelido == best_option), col + 'pontos'] = linha.pontuacao

            else:
                print(
                    f"COROI, cara gagazeiro o {linha.apelido}, na iniciativa {linha.iniciativa} tem {linha.pontuacao} pontos")

        elif df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option), 'pontos_iniciativas_I2_pontos'].values[0] != "":
            df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option),
                                       'pontos_iniciativas_I3_nome'] = linha['iniciativa']
            df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option),
                                       'pontos_iniciativas_I3_pontos'] = linha['pontuacao']

        else:
            df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option),
                                       'pontos_iniciativas_I2_nome'] = linha['iniciativa']
            df_summary_iniciativas.loc[(df_summary_iniciativas.apelido == best_option),
                                       'pontos_iniciativas_I2_pontos'] = linha['pontuacao']

    else:
        df_summary_iniciativas = pd.concat([df_summary_iniciativas, pd.DataFrame(
            {
                'nome': linha['nome'],
                'apelido': linha['apelido'],
                'pontos_iniciativas_I1_nome': linha['iniciativa'],
                'pontos_iniciativas_I1_pontos': linha['pontuacao'],
                'pontos_iniciativas_I2_nome': "",
                'pontos_iniciativas_I2_pontos': 0,
                'pontos_iniciativas_I3_nome': "",
                'pontos_iniciativas_I3_pontos': 0
            }, index=[0])], ignore_index=True)


df_summary_iniciativas.sort_values(by='nome', ascending=False, inplace=True)
df_summary_iniciativas.reset_index(inplace=True, drop=True)
df_summary_iniciativas


df_summary_iniciativas.replace(to_replace=0, value='', inplace=True)
df_summary_iniciativas.sort_values(by='nome', inplace=True)

# export to sheets
export = sh.worksheet('summary_iniciativas')
export.clear()

i = 2
export.update('A1', 'Soma de pontos por iniciativa,  Dividida por iniciativa')
export.update(f"B{i}:I{not_described_sum.shape[0] + i}", [
              df_summary_iniciativas.columns.values.tolist()] + df_summary_iniciativas.values.tolist())


df_summary_iniciativas
