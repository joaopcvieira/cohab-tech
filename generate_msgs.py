from templates import *
import numpy as np
import gspread

import chat_bot_Selenium as selenium
import twilio_sender as twilio

import alunos_info


def main():
    # alunos = alunos_info.get_students_info()
    # alunos['mnsg_enviada'] = False

    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("Alunos db")
    ws = sh.worksheet("H8 + info boletos")


    alunos = pd.DataFrame(ws.get("A3:Y"), columns=ws.get("A2:Y2")[
                        0]).dropna(subset=['nome'])
    mensagens = list()
    for idx, linha in alunos.iterrows():
        if linha.meses_devendo != '-':
            mensagens.append(msg_dever_boletos_sheets(linha))
        else:
            # mensagens.append(msg_validacao_pontos_sheets(linha))
            mensagens.append("")    
            

    alunos_info.update_mnsg_sheets_manual_check(np.array([mensagens]))


    # devendo = alunos[alunos.meses_devendo != '-']
    # devendo['mensagens'] = devendo.apply(lambda x: msg_dever_boletos_wpp(x), axis=1)

        
        

if __name__ == '__main__':
    main()
