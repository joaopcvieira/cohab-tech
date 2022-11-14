import aux_funcs as aux
from alunos_info import get_students_info
import pandas as pd
import gspread
import aux_funcs as aux

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
green = bcolors.GREEN
red = bcolors.RED
yellow = bcolors.YELLOW
bold = bcolors.BOLD
end = bcolors.ENDC


def fix_df(df: pd.DataFrame, tamanho: int) -> pd.DataFrame:
    df['celular'] = df['celular'].apply(aux.fix_cel)
    for i in range(1, tamanho + 1):
        coluna = 'cpf_' + str(i)
        df[coluna] = df[coluna].apply(aux.fix_cpf)
    
    return df

def get_pontuacao_por_ap(df_forms: pd.DataFrame, tamanho: int) -> pd.DataFrame:
    pontos_total = []
    devendo_total = []
    alunos_pontuacao = get_students_info(
    )[['nome', 'apelido', 'cpf', 'pontos_total', 'meses_devendo']]
    alunos_pontuacao['nome'] = alunos_pontuacao.nome.apply(
        aux.remove_accents_and_special_characters)
    alunos_pontuacao.cpf = alunos_pontuacao.cpf.apply(aux.fix_cpf)

    for i in range(1, tamanho):
        coluna = 'cpf_' + str(i)
        df_forms[coluna] = df_forms[coluna].apply(aux.fix_cpf)

    df_forms.dropna(subset=['nome_1'], inplace=True)
    for idx, linha in df_forms.iterrows():
        pontos = tamanho * 1000 
        devendo = 0

        for i in range(1, tamanho + 1):
            coluna = 'cpf_' + str(i)
            # aluno_nome = aux.remove_accents_and_special_characters(linha[coluna])
            aluno_cpf = aux.fix_cpf(linha[coluna])
            if(aluno_cpf != ''):
                try:
                    pontos += alunos_pontuacao[alunos_pontuacao.cpf ==
                                               aluno_cpf].pontos_total.apply(aux.fix_number).values[0]
                    if alunos_pontuacao[alunos_pontuacao.cpf == aluno_cpf].meses_devendo.values[0] != '-':
                        devendo += 1
                except:
                    print(
                        f'Aluno {aluno_cpf} não encontrado. Problema na linha: {idx}')
                    pontos = 0
                    break
            if(aluno_cpf == 'ERRO CPF INVALIDO'):
                col = 'nome_' + str(i)
                print(f'{linha[col]} está com cpf inválido. Problema na linha: {idx}')

        pontos_total.append(pontos)
        devendo_total.append(devendo)

    df_forms['pontos_total'] = pontos_total
    df_forms['devendo'] = devendo_total
    return df_forms.sort_values(by=['devendo', 'pontos_total'], ascending=False)

def get_vagas_disponiveis() -> pd.DataFrame:
    sa = gspread.service_account(filename='credentials.json')
    sh = sa.open("H8 - 2022.2")
    # ws = sh.worksheet("H8 2022.2")
    # vagas = pd.DataFrame(ws.get("A2:F"), columns=ws.get("A1:F1")[0])
    vagas = sh.worksheet("H8 2022.2").get_all_values()
    vagas_df = pd.DataFrame(vagas[1:], columns=vagas[0])
    vagas_df = vagas_df[vagas_df.NOME.str.contains('VAGA')]
    vagas_df.rename(columns={
        'ALOJ': 'ap_bloco',
        'NOME': 'nome',
        'APTO': 'ap_numero',
        'Apelido': 'apelido',
        'VAGA': 'ap_vaga',
        'T': 'turma'
    }, inplace=True)
    vagas_df['ap_bloco'] = vagas_df['ap_bloco'].apply(lambda x: x[3:])
    vagas_df['ap_match'] = vagas_df.apply(lambda x: x.ap_bloco + x.ap_numero, axis=1)
    vagas_df['vaga_match'] = vagas_df.apply(lambda x: x.ap_bloco + x.ap_numero + ', vaga ' + x.ap_vaga, axis=1)

    vagas_por_ap = vagas_df.groupby('ap_match').count().reset_index()[['ap_match', 'ap_vaga']]
    vagas_df['vagas_por_ap'] = vagas_df['ap_match'].apply(lambda x: vagas_por_ap[vagas_por_ap.ap_match == x].ap_vaga.values[0])

    return vagas_df.drop(columns=['apelido', 'turma'])

def check_option_available(tamanho: int, apartamento: str, vaga: str, vagas_df: pd.DataFrame) -> bool:
    if tamanho == 4 or tamanho == 6:
        if apartamento in vagas_df.vaga_match.values:
            return True
        else:
            return False

    else:
        if apartamento not in vagas_df.ap_match.values:
            return False
        else:
            ap = vagas_df[vagas_df.ap_match == apartamento]
            
            if tamanho == 1:
                if vaga in ap.ap_vaga.values:
                    return True
                else:
                    return False

            elif tamanho == 2:
                vaga_1, vaga_2 = vaga.split(' e ')
                if vaga_1 in ap.ap_vaga.values and vaga_2 in ap.ap_vaga.values:
                    return True
                else:
                    return False

def run_postulacao_duplas(dupla_df: pd.DataFrame) -> tuple:
    # alunos_tout = get_students_info()
    trocou = list()
    opcao_troca = list()
    vagas_df = get_vagas_disponiveis()

    for idx, linha in dupla_df.iterrows():
        print(f'\nVerificando {linha.nome_1} e {linha.nome_2}')

        for i in range(3):
            it = i + 1
            if(linha[f'bloco_{it}'] == "Não tenho essa opção"):
                trocou.append(False)
                opcao_troca.append(0)
                print(
                    f'\tOpção {it}:  Ø \tnão conseguiram {bold}{red}NENHUM{end} ap')
                break
            else:
                ap_match = linha[f'bloco_{it}'] + linha[f'opcao_{it}']
                vagas = linha[f'vaga_{it}']
                vaga_1, vaga_2 = vagas.split(' e ')
                if(check_option_available(2, ap_match, vagas, vagas_df)):
                    trocou.append(True)
                    print(
                        f'\t{green}Opção {it}{end}: {green}ap{linha[f"opcao_{it}"]}{end} disponível')
                    opcao_troca.append(it)
                    vagas_df = vagas_df[vagas_df.vaga_match !=
                                        f'{ap_match}, vaga {vaga_1}']
                    vagas_df = vagas_df[vagas_df.vaga_match !=
                                        f'{ap_match}, vaga {vaga_2}']
                    break
                else:
                    print(
                        f'\t{yellow}Opção {it}{end}: não conseguiram o {yellow}ap{linha[f"opcao_{it}"]}{end}')
                    if it == 3:
                        print(
                            f'\tnão conseguiram {bold}{red}NENHUM{end} ap')
                        trocou.append(False)
                        opcao_troca.append(0)
                        break

    dupla_df['trocou'] = trocou
    dupla_df['opcao_troca'] = opcao_troca

    alunos_duplas = pd.DataFrame(
        columns=['nome', 'cpf', 'ap_bloco', 'ap_numero', 'ap_vaga', 'ap_pontuacao'])
    for idx, linha in dupla_df.iterrows():
        if linha.opcao_troca == 0:
            aluno_1 = alunos_tout[alunos_tout.cpf == linha.cpf_1]
            A1 = pd.DataFrame(
                {'nome': aluno_1.nome.values[0], 'cpf': aluno_1.cpf.values[0], 'ap_bloco': aluno_1.ap_bloco.values[0],
                 'ap_numero': aluno_1.ap_numero.values[0], 'ap_vaga': aluno_1.ap_vaga.values[0],
                 'ap_pontuacao': linha.pontos_total}, index=[0]
            )
            aluno_2 = alunos_tout[alunos_tout.cpf == linha.cpf_2]
            A2 = pd.DataFrame(
                {'nome': aluno_2.nome.values[0], 'cpf': aluno_2.cpf.values[0], 'ap_bloco': aluno_2.ap_bloco.values[0],
                 'ap_numero': aluno_2.ap_numero.values[0], 'ap_vaga': aluno_2.ap_vaga.values[0],
                 'ap_pontuacao': linha.pontos_total}, index=[0]
            )

            alunos_duplas = pd.concat([alunos_duplas, A1])
            alunos_duplas = pd.concat([alunos_duplas, A2])

        else:
            A1 = pd.DataFrame(
                {'nome': linha.nome_1, 'cpf': linha.cpf_1, 'ap_bloco': linha[f'bloco_{linha.opcao_troca}'],
                 'ap_numero': linha[f'opcao_{linha.opcao_troca}'], 'ap_vaga': linha[f'vaga_{linha.opcao_troca}'],
                 'ap_pontuacao': linha.pontos_total}, index=[0]
            )
            A2 = pd.DataFrame(
                {'nome': linha.nome_2, 'cpf': linha.cpf_2, 'ap_bloco': linha[f'bloco_{linha.opcao_troca}'],
                 'ap_numero': linha[f'opcao_{linha.opcao_troca}'], 'ap_vaga': linha[f'vaga_{linha.opcao_troca}'],
                 'ap_pontuacao': linha.pontos_total}, index=[0]
            )

            alunos_duplas = pd.concat([alunos_duplas, A1])
            alunos_duplas = pd.concat([alunos_duplas, A2])

    return dupla_df, alunos_duplas

def run_postulacao_sozinhos(sozinho_df: pd.DataFrame) -> tuple:
    # alunos_tout = get_students_info()
    trocou = list()
    opcao_troca = list()
    vagas_df = get_vagas_disponiveis()

    for idx, linha in sozinho_df.iterrows():
        print(f'\nVerificando {linha.nome_1}')

        for i in range(3):
            it = i + 1

            if(linha[f'bloco_{it}'] == "Não tenho essa opção"): # Se não tem outra opção
                trocou.append(False)
                opcao_troca.append(0)
                print(
                    f'\t{red}Opção {it}{end}:  Ø \t Não conseguiu {bold}{red}NENHUM{end} ap')
                break

            else:
                ap_match = linha[f'bloco_{it}'] + linha[f'opcao_{it}']
                vaga = linha[f'vaga_{it}']

                if(check_option_available(1, ap_match, vaga, vagas_df)): # aluno conseguiu ap
                    trocou.append(True)

                    print(
                        f'\t{green}Opção {it}{end}: {green}ap{linha[f"opcao_{it}"]}{end} disponível')

                    opcao_troca.append(it)
                    vagas_df = vagas_df[vagas_df.vaga_match != f'{ap_match}, vaga {vaga}']
                    break

                else:
                    print(
                        f'\t{yellow}Opção {it}{end}: não conseguiu o {bold}ap{linha[f"opcao_{it}"]}{end}')
                    if it == 3:
                        print(
                            f' \tnão conseguiu {bold}{red}NENHUM{end} ap')
                        trocou.append(False)
                        opcao_troca.append(0)
                        break

    sozinho_df['trocou'] = trocou
    sozinho_df['opcao_troca'] = opcao_troca

    alunos_duplas = pd.DataFrame(
        columns=['nome', 'cpf', 'ap_bloco', 'ap_numero', 'ap_vaga', 'ap_pontuacao'])

    for idx, linha in sozinho_df.iterrows():

        if linha.opcao_troca == 0:
            aluno = alunos_tout[alunos_tout.cpf == linha.cpf_1]
            A1 = pd.DataFrame({
                'nome': aluno.nome.values[0], 'cpf': aluno.cpf.values[0], 'ap_bloco': aluno.ap_bloco.values[0],
                'ap_numero': aluno.ap_numero.values[0], 'ap_vaga': aluno.ap_vaga.values[0],
                'ap_pontuacao': linha.pontos_total
            }, index=[0])
            alunos_duplas = pd.concat([alunos_duplas, A1])

        else:
            A1 = pd.DataFrame({
                'nome': linha.nome_1, 'cpf': linha.cpf_1, 'ap_bloco': linha[f'bloco_{linha.opcao_troca}'],
                'ap_numero': linha[f'opcao_{linha.opcao_troca}'], 'ap_vaga': linha[f'vaga_{linha.opcao_troca}'],
                'ap_pontuacao': linha.pontos_total
            }, index=[0])
            alunos_duplas = pd.concat([alunos_duplas, A1])

    return sozinho_df, alunos_duplas

if __name__ == "__main__":
    sa = gspread.service_account(filename='credentials.json')
    postulacao = sa.open("Respostas Postulação Cohab 2022.2")
    sozinho = postulacao.worksheet("1_pessoa").get_all_values()
    dupla = postulacao.worksheet("2_pessoas").get_all_values()
    quarteto = postulacao.worksheet("4_pessoas").get_all_values()
    sexteto = postulacao.worksheet("6_pessoas").get_all_values()

    sozinho_df = fix_df(pd.DataFrame(sozinho[1:], columns=sozinho[0]), 1)
    dupla_df = fix_df(pd.DataFrame(dupla[1:], columns=dupla[0]), 2)
    quarteto_df = fix_df(pd.DataFrame(quarteto[ 1:], columns=quarteto[0]), 4)
    sexteto_df = fix_df(pd.DataFrame(sexteto[1:], columns=sexteto[0]), 6)

    sozinho_df = get_pontuacao_por_ap(sozinho_df, 1)
    sozinho_df = sozinho_df.reset_index(drop=True)

    dupla_df = get_pontuacao_por_ap(dupla_df, 2)
    dupla_df = dupla_df.reset_index(drop=True)

    vagas = get_vagas_disponiveis()
    vagas_2 = vagas[vagas.vagas_por_ap >= 2]


    alunos_tout = get_students_info()


    # run_postulacao_duplas(dupla_df)
    run_postulacao_sozinhos(sozinho_df)

    pass