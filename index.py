from templates import *
from send_email import send_email
from alunos_info import get_students_info
from boletos_infos import boletos_infos


def main():
    alunos = get_students_info()
    alunos['email_enviado'] = False
    devendo_boletos = boletos_infos()

    for idx, linha in alunos.iterrows():
        if idx == 0:
            pass

        elif linha.devendo_boletos != '':
            print(msg_dever_boletos(linha))
        # elif linha.cpf in devendo_boletos.cpf.values:
        #     aluno_devendo = devendo_boletos.loc[devendo_boletos.cpf == linha.cpf]
        #     aluno_devendo = aluno_devendo.reset_index(drop=True).iloc[0]
        #     print("O cara q ta devendo é o ", aluno_devendo.nome)
        #     # print(aluno_devendo.head())
        #     send_email(linha.email, msg_dever_boletos(linha))
        #     break
        else:
            send_email(linha.email, msg_validacao_pontos(linha))
            print("Email enviado para ", linha.nome)
            alunos.loc[idx, 'email_enviado'] = True

        # if idx == 1:
            # break


if __name__ == '__main__':
    main()
