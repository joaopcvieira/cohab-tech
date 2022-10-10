import json
import pandas as pd
import gspread


def alunos_presentes_nas_ags() -> pd.DataFrame:
    sa = gspread.service_account(filename='credentials.json')
    planilha_AG = sa.open('Presença na AG').worksheet("Geral")

    col = ['nome', 'apelido', 'turma', '26/05', 'x', '20/06', 'y', '08/09']
    presenca_AG = pd.DataFrame(
        data=planilha_AG.get("A4:H"),
        columns=col
    )

    presenca_AG.drop('x', axis=1, inplace=True)
    presenca_AG.drop('y', axis=1, inplace=True)

    presenca_AG = presenca_AG.loc[(presenca_AG['26/05'] == 'TRUE') &
                                  (presenca_AG['20/06'] == 'TRUE') &
                                  (presenca_AG['08/09'] == 'TRUE')]
    return presenca_AG

# print(alunos_presentes_nas_ags().head())
