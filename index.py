from templates import *
import numpy as np

# from send_email import send_email
# from api_wpp import send_message
# from chat_bot_Selenium import send_messages_selenium
import chat_bot_Selenium as selenium
import twilio_sender as twilio

import alunos_info
from boletos_infos import boletos_infos


def main():
    alunos = alunos_info.get_students_info()
    alunos['mnsg_enviada'] = False
    devendo_boletos = boletos_infos()

    mensagens = list()
    for idx, linha in alunos.iterrows():
        if linha.meses_devendo != '-':
            mensagens.append(msg_dever_boletos_sheets(linha))
           
            # try:
            #     print(f'O telefone foi {linha.celular}')
            #     twilio.send_message(msg_dever_boletos(linha), f'{linha.celular}')
            #     print(f'Mensagem enviada para {linha.nome}')
            #     linha.update({'mnsg_enviada': True})
            # except:
            #     print(f'Erro ao enviar mensagem para {linha.nome}. Ele DEVE boletos.')
            # break

        else:
            mensagens.append("")
            # mensagens.append(msg_validacao_pontos_sheets(linha))
            
            # # send_email(linha.email, msg_validacao_pontos(linha))
            # print(f'O telefone foi {linha.celular}')
            # twilio.send_message(msg_validacao_pontos(linha), f'{linha.celular}')
            # # send_message(msg_resultado_alocacao(linha), f'{linha.celular}')
            # # print("Mnsg enviada para ", linha.nome)
            # alunos.loc[idx, 'mnsg_enviada'] = True
    alunos_info.update_mnsg_sheets_manual_check(np.array([mensagens]))


    devendo = alunos[alunos.meses_devendo != '-']
    devendo['mensagens'] = devendo.apply(lambda x: msg_dever_boletos_wpp(x), axis=1)
    # selenium.send_messages_selenium(devendo)

        
        

if __name__ == '__main__':
    main()
