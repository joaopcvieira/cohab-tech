import pandas as pd


def msg_validacao_pontos(linha=pd.Series()) -> str:
    validacao_pontos = '''
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
  </head>
  <body>

    <h3>Validação dos pontos</h3>

    <h4>Olá, {nome}! </h4>

    <p>Seus pontos foram validados com sucesso! Você apresentou no final, um total de <i>{pontos_total} pontos.</i></p>
    <br>
    <p>Segue abaixo a divisão e origem dessa pontuação:</p>
    <br> '''.format(**linha)

    if(linha.pontos_presenca != 0 and linha.pontos_presenca != None):
        validacao_pontos += '''
    <p>Presença em AG's: {pontos_presenca}</p>'''.format(**linha)

    if(linha.pontos_boletos != 0 and linha.pontos_boletos != None):
        validacao_pontos += '''
    <p>Boletos pagos: {pontos_boletos}</p>'''.format(**linha)

    if(linha.pontos_iniciativas_I1_pontos != 0 and linha.pontos_iniciativas_I1_pontos != None):
        validacao_pontos += '''
    <h4>Iniciativas </h4>
    <p> <strong>{pontos_iniciativas_I1_nome}</strong>: <br/>
    Correspondentes a um total de {pontos_iniciativas_I1_pontos} pontos. </p>'''.format(**linha)

    if(linha.pontos_iniciativas_I2_pontos != 0 and linha.pontos_iniciativas_I2_pontos != None):
        validacao_pontos += '''
    <p> <strong>{pontos_iniciativas_I2_nome}</strong>: <br/>
    Correspondentes a um total de {pontos_iniciativas_I2_pontos} pontos. </p>'''.format(**linha)

    if(linha.pontos_iniciativas_I3_pontos != 0 and linha.pontos_iniciativas_I3_pontos != None):
        validacao_pontos += '''
    <p> <strong>{pontos_iniciativas_I3_nome}</strong>: <br/>
    Correspondentes a um total de {pontos_iniciativas_I3_pontos} pontos. </p>'''.format(**linha)

    validacao_pontos += '''
    <p>Qualquer dúvida ou sugestão a respeito da validação dos pontos, estamos à disposição,</p>

    <p>Isabel, Begis T-25<br/>
    Diretora da Cohab.</p>

  </body>
</html>
 '''
    return validacao_pontos


def msg_resultado_alocacao(linha = pd.Series()) -> str:
    resultado_alocacao = '''
<!DOCTYPE html>
<html>
<head>
    <base target = "_top">
</head>
<body>

    <h3>Resultado da Postulação</h3>

    <h4>Parabéns, {nome}!</h4>

    <p>Você conseguiu postular para a vaga {ap_vaga}, do apartamento {ap_numero}, bloco {ap_bloco}!</p>

    <p> Qualquer dúvida ou sugestão, estamos à disposição,</p>
    <p> Isabel Alencar Tavares Colares Brasil, <br/>
        Diretora da CoHab.</p>


</body>
</html> '''
    return resultado_alocacao.format(**linha)


def msg_dever_boletos(linha = pd.Series()) -> str:
    dever_boletos = '''
<!DOCTYPE html>
<html>
	<head>
		<base target="_top">
	</head>
	<body>
		<h4>Olá, {nome}</h4>

		<p>No tocante ao corrente processo de postulação, recebemos o seu pedido de postulação referente às vagas {VAGAS}
        <!-- $vagas, talvez listadas ... usar um concat e show -->
        .</p>

		<p>Entretanto, notamos aqui que você está com pendências em relação ao pagamento da taxa de manutenção do H8, e isso configura um impedimento para a sua participação no processo de escolha de vagas.</p>

		<p>Constam como não pagos os boletos referentes à {MESES}.</p>

		<p>Orientamos que você entre em contato com o Financeiro do Casd, seja através do WhatsApp do Financeiro (12)98142-6646 - (Sheyla), ou se dirigindo até a Sala do Casd para que acerte as suas pendências e dê seguimento ao processo de postulação.</p>

		<p>O <strong>prazo final</strong> para a resolução das pendências, mantendo o requerimento de postulação, é: <strong>***<!--PRAZO--></strong>.</p>

		<p>Ressaltamos ainda que o pagamento da taxa de manutenção, previsto na NPA ***<!--Npa de moradia...-->, é de suma importância para a realização de obras e projetos no H8, então mesmo que tenha mudado de ideia e não queira dar prosseguimento à postulação, realize o pagamento mesmo assim.</p>

		<p>Qualquer dúvida ou sugestão, estamos à disposição,</p>

		<p>
			<strong>
				Isabel Brasil,<br/>
				Diretora da COHAB - Casd
			</strong>
		</p>

	</body>
</html>'''
    return dever_boletos.format(**linha)


# print(msg_validacao_pontos(aluno))





# aluno = {
#     'nome': 'João Pedro',
#     'apelido': 'João',
#     'turma': 'T25',
#     'cpf': '123.456.789-00',
#     'email': 'meuemail@gmail.com',
#     'ap': {
#         'numero': '123',
#         'bloco': 'A',
#         'vaga': 'D'
#     },
#     'pontos': {
#         'total': 10,
#         'presenca': 0,
#         'boletos': 0,
#         'iniciativas': {
#             'I1': {
#                 'nome': 'Iniciativa 1',
#                 'pontos': 0
#             },
#             'I2': {
#                 'nome': 'Iniciativa 2',
#                 'pontos': 0
#             },
#             'I3': {
#                 'nome': 'Iniciativa 3',
#                 'pontos': 0
#             },
#         }
#     }
# }