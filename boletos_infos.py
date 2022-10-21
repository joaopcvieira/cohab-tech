import pandas as pd
import gspread

def boletos_infos() -> pd.DataFrame:
    sa = gspread.service_account(filename='credentials.json')
    planilha_boletos = sa.open('Cópia de Controle Mensalidade - Base de dados').worksheet('export_python')
    
    col = ['nome', 'turma', 'email', 'apelido', 'cpf', 'meses_devendo', 'ap_bloco_boletos', 'ap_numero_boletos', 'ap_vaga_boletos']
    
    data = planilha_boletos.get("A2:I")
    boletos = pd.DataFrame(columns=col, data=data)

    devendo_boletos = boletos.loc[(boletos.meses_devendo != '') & (boletos.meses_devendo.notnull())]
    devendo_boletos.to_csv('boletos_devendo.csv', index=False)

    return devendo_boletos

# print(boletos_infos().head())
# boletos_infos().to_csv('boletos_devendo.csv', index=False)