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

def msg_validacao_pontos(linha):
    validacao_pontos = '''
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
  </head>
  <body>
   
    <h3>Validação dos pontos</h3>
    
    <h4>Olá, {linha.nome}! </h4>
'''

#     <p>Seus pontos foram validados com sucesso! Você apresentou no final, um total de <i>{aluno['pontos']['total']}.</i></p>
#     <br>
#     <p>Segue abaixo a divisão e origem dessa pontuação:</p>
#     <br> '''
    
#     if(aluno['pontos']['presenca']):
#         validacao_pontos += '''
#     <p>Presença em AG's: {aluno['pontos']['presenca']}</p>'''
    
#     if(aluno['pontos']['boletos']):  
#         validacao_pontos += '''
#     <p>Boletos pagos: {aluno['pontos']['boletos']}</p>'''

#     if(aluno['pontos']['iniciativas']['I1']['pontos']):
#         validacao_pontos += '''
#     <h4>Iniciativas </h4>
#     <p> {aluno['pontos']['iniciativas']['I1']['nome']} <br/>
#     Correspondentes a um total de {aluno['pontos']['iniciativas']['I1']['pontos']} pontos. </p>'''

#     if(aluno['pontos']['iniciativas']['I2']['pontos']):
#         validacao_pontos += '''
#     <p> {aluno['pontos']['iniciativas']['I2']['nome']} <br/>
#     Correspondentes a um total de {aluno['pontos']['iniciativas']['I2']['pontos']} pontos. </p>'''

#     if(aluno['pontos']['iniciativas']['I3']['pontos']):
#         validacao_pontos += '''
#     <p> {aluno['pontos']['iniciativas']['I3']['nome']} <br/>
#     Correspondentes a um total de {aluno['pontos']['iniciativas']['I3']['pontos']} pontos. </p>'''


#     validacao_pontos +='''
#     <p>Qualquer dúvida ou sugestão a respeito da validação dos pontos, estamos à disposição,</p>

#     <p>Isabel, Begis T-25<br/>
#     Diretora da Cohab.</p>
    
#   </body>
# </html>
# '''
    return validacao_pontos.format(linha=linha)

def msg_resultado_alocacao(linha):
    resultado_alocacao = '''
<!DOCTYPE html>
<html>
<head>
    <base target = "_top">
</head>
<body>

    <h3>Resultado da Postulação</h3>

    <h4>Parabéns, {aluno.name}!</h4>

    <p>Você conseguiu postular para a vaga {aluno.ap.vaga}, do apartamento {aluno.ap.numero}!</p>

    <p> Qualquer dúvida ou sugestão, estamos à disposição,</p>
    <p> Isabel Alencar Tavares Colares Brasil, <br/>
        Diretora da CoHab.</p>
    

</body>
</html> '''
    return resultado_alocacao.format(linha=linha)

def msg_dever_boletos(linha):
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
# .format(NOME=..., VAGAS=..., MESES=...)


# print(msg_validacao_pontos(aluno))

    print('teste de {nome}'.format(**linha))
    return msg_validacao_pontos(linha)