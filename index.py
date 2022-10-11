from templates import *

from send_email import send_email
from api_wpp import send_message
from chat_bot_Selenium import send_messages_selenium

from alunos_info import get_students_info
from boletos_infos import boletos_infos


def main():
    alunos = get_students_info()
    alunos['mnsg_enviada'] = False
    devendo_boletos = boletos_infos()

    for idx, linha in alunos.iterrows():
        if idx == 0:
            pass

        elif linha.meses_devendo != '':
            # print(msg_dever_boletos(linha))
            send_message(msg_dever_boletos(linha), f'{linha.celular}')
            linha.update({'mnsg_enviada': True})
            break

        else:
            # send_email(linha.email, msg_validacao_pontos(linha))
            send_message(msg_validacao_pontos(linha), f'{linha.celular}')
            send_message(msg_resultado_alocacao(linha), f'{linha.celular}')
            print("Mnsg enviada para ", linha.nome)
            alunos.loc[idx, 'mnsg_enviada'] = True

        # if idx == 1:
        #     break


if __name__ == '__main__':
    main()
