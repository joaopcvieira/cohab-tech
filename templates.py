import pandas as pd

DATA_MAX_BOLETOS = '08/11/2022'

def msg_validacao_pontos_wpp(linha) -> str:
    validacao_pontos = '''
*Postulação 2022*
*Validação dos pontos*

Olá, {nome}! 
Seus pontos foram validados com sucesso! Você apresentou no final, um total de _{pontos_total} pontos._

Segue abaixo a divisão e origem dessa pontuação: '''.format(**linha)

    if(linha.pontos_antigos != 0 and linha.pontos_antigos != None):
        validacao_pontos += '''
        Pontuação Anterior ao ano corrente: {pontos_antigos}'''.format(**linha)
    
    if(linha.pontos_presenca != 0 and linha.pontos_presenca != None):
        validacao_pontos += '''
        Presença em AG's: {pontos_presenca}'''.format(**linha)

    if(linha.pontos_boletos != 0 and linha.pontos_boletos != None):
        validacao_pontos += '''
        Boletos pagos: {pontos_boletos}'''.format(**linha)

    if(linha.pontos_iniciativas_I1_pontos != 0 and linha.pontos_iniciativas_I1_pontos != None):
        validacao_pontos += '''

    *Iniciativas* 

    *{pontos_iniciativas_I1_nome}*:
    Correspondentes a um total de _{pontos_iniciativas_I1_pontos} pontos._'''.format(**linha)

    if(linha.pontos_iniciativas_I2_pontos != 0 and linha.pontos_iniciativas_I2_pontos != None):
        validacao_pontos += '''
    *{pontos_iniciativas_I2_nome}*:
    Correspondentes a um total de _{pontos_iniciativas_I2_pontos} pontos._'''.format(**linha)

    if(linha.pontos_iniciativas_I3_pontos != 0 and linha.pontos_iniciativas_I3_pontos != None):
        validacao_pontos += '''

    *{pontos_iniciativas_I3_nome}*:
    Correspondentes a um total de _{pontos_iniciativas_I3_pontos} pontos._'''.format(**linha)

    if(linha.pontos_extra != 0 and linha.pontos_extra != None):
        validacao_pontos += '''
        Pontuação Extra: {pontos_extra} pontos.'''.format(**linha)

    validacao_pontos += '''
    Qualquer dúvida ou sugestão a respeito da validação dos pontos, estamos à disposição,

    Comissão de Habitação (CoHab).
 '''
    return validacao_pontos

def msg_resultado_alocacao_wpp(linha) -> str:
    resultado_alocacao = '''
*Postulação 2022*
*Resultado da Postulação*

Parabéns, {nome}!
Você conseguiu postular para a *vaga {ap_vaga}, do apartamento {ap_numero}, bloco {ap_bloco}!*

Qualquer dúvida ou sugestão, estamos à disposição,

Comissão de Habitação (CoHab).
'''
    return resultado_alocacao.format(**linha)


def msg_dever_boletos_wpp(linha) -> str:
    dever_boletos = '''
*Postulação 2022*

*Olá, {nome}!*

Recebemos o seu pedido de postulação.
Entretanto, notamos aqui que você está com *pendências* em relação ao pagamento da taxa de manutenção do H8. Segundo o regimento interno da CoHab, para postular é necessário estar em dia com o pagamento da mensalidade do Casd.
Constam como não pagos os boletos referentes à 

    {meses_devendo}.'''.format(**linha)
    dever_boletos+='''
    
Orientamos que você entre em contato com o Financeiro do Casd, seja através do WhatsApp do Financeiro (12) 98142-6646 (Sheyla), ou se dirigindo até a sala do Casd para que acerte as suas pendências e dê seguimento ao processo de postulação.

O *prazo final* para a resolução das pendências, mantendo o requerimento de postulação, é: *{data}*.
Ressaltamos ainda que o pagamento da taxa de manutenção, previsto na NPA 045, é de suma importância para a realização de obras e projetos no H8, então mesmo que tenha mudado de ideia e não queira dar prosseguimento à postulação, realize o pagamento mesmo assim.
Qualquer dúvida ou sugestão, estamos à disposição,


   
    Comissão de Habitação (CoHab).
	'''.format(data=DATA_MAX_BOLETOS)
    return dever_boletos

def msg_validacao_pontos_sheets(linha) -> str:
    validacao_pontos = '''
Postulação 2022
Validação dos pontos

Olá, {nome}! 
Seus pontos foram validados com sucesso! Você apresentou no final, um total de {pontos_total} pontos.

Segue abaixo a divisão e origem dessa pontuação: '''.format(**linha)

    if(linha.pontos_antigos != 0 and linha.pontos_antigos != '0' and linha.pontos_antigos != None):
        validacao_pontos += '''
    Pontuação Anterior ao ano corrente: {pontos_antigos}
        '''.format(**linha)
    
    if(linha.pontos_presenca != 0 and linha.pontos_presenca != '0' and linha.pontos_presenca != None):
        validacao_pontos += '''
    Presença em AG's: {pontos_presenca}
        '''.format(**linha)

    if(linha.pontos_boletos != 0 and linha.pontos_boletos != '0' and linha.pontos_boletos != None):
        validacao_pontos += '''
        Pontuação por adimplência + anuidade paga: {pontos_boletos}'''.format(**linha)

    if(linha.pontos_iniciativas_I1_pontos != 0 and linha.pontos_iniciativas_I1_pontos != '0' and linha.pontos_iniciativas_I1_pontos != None):
        validacao_pontos += '''

    Iniciativas 

    {pontos_iniciativas_I1_nome}: {pontos_iniciativas_I1_pontos} pontos.'''.format(**linha)

    if(linha.pontos_iniciativas_I2_pontos != 0 and linha.pontos_iniciativas_I2_pontos != '0' and linha.pontos_iniciativas_I2_pontos != None):
        validacao_pontos += '''

    {pontos_iniciativas_I2_nome}: {pontos_iniciativas_I2_pontos} pontos.'''.format(**linha)

    if(linha.pontos_iniciativas_I3_pontos != 0 and linha.pontos_iniciativas_I3_pontos != '0' and linha.pontos_iniciativas_I3_pontos != None):
        validacao_pontos += '''

    {pontos_iniciativas_I3_nome}: {pontos_iniciativas_I3_pontos} pontos.
    '''.format(**linha)

    if(linha.pontos_extra != 0 and linha.pontos_extra != '0' and linha.pontos_extra != None):
        validacao_pontos += '''
        
    Pontuação Extra: {pontos_extra} pontos.
    Pontuação extra inclui pontuação da CR 26, representantes e outros, caso se aplique.
'''.format(**linha)

    validacao_pontos += '''

Qualquer dúvida ou sugestão a respeito da validação dos pontos, estamos à disposição,

    Silveirinha T-25
    Casd.
 '''
    return validacao_pontos

def msg_resultado_alocacao_sheets(linha) -> str:
    resultado_alocacao = '''
Postulação 2022
Resultado da Postulação

Parabéns, {nome}!
Você conseguiu postular para a vaga {ap_vaga}, do apartamento {ap_numero}, bloco {ap_bloco}!

Qualquer dúvida ou sugestão, estamos à disposição,

Comissão de Habitação (CoHab).
'''
    return resultado_alocacao.format(**linha)


def msg_dever_boletos_sheets(linha) -> str:
    dever_boletos = '''
Postulação 2022

Olá, {nome}!

Recebemos o seu pedido de postulação.
Entretanto, notamos aqui que você está com pendências em relação ao pagamento da taxa de manutenção do H8. Segundo o regimento interno da CoHab, para postular é necessário estar em dia com o pagamento da mensalidade do Casd.
Constam como não pagos os boletos referentes à 
    {meses_devendo}.'''.format(**linha)
    dever_boletos+='''

Orientamos que você entre em contato com o Financeiro do Casd, seja através do WhatsApp do Financeiro (12) 98142-6646 (Sheyla), ou se dirigindo até a sala do Casd para que acerte as suas pendências e dê seguimento ao processo de postulação.
O prazo final para a resolução das pendências, mantendo o requerimento de postulação, é: {data}.

Ressaltamos ainda que o pagamento da taxa de manutenção, previsto na NPA 045, é de suma importância para a realização de obras e projetos no H8, então mesmo que tenha mudado de ideia e não queira dar prosseguimento à postulação, realize o pagamento mesmo assim.
Qualquer dúvida ou sugestão, estamos à disposição,


   
    Comissão de Habitação (CoHab).
	'''.format(data=DATA_MAX_BOLETOS)
    return dever_boletos.format(**linha)




def msg_validacao_pontos_html(linha) -> str:
    validacao_pontos = '''
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
  </head>
  <body>

    <h3>Validação dos pontos</h3>

    <h4>Olá, {nome}! </h4>

    Seus pontos foram validados com sucesso! Você apresentou no final, um total de <i>{pontos_total} pontos.</i></p>
    <br>
    <p>Segue abaixo a divisão e origem dessa pontuação:</p>
    <br> '''.format(**linha)

    if(linha.pontos_antigos != 0 and linha.pontos_antigos != None):
        validacao_pontos += '''
    <p>Pontuação Anterior ao ano corrente: {pontos_antigos}</p>'''.format(**linha)
    
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

    <p>Comissão de Habitação (CoHab).</p>

  </body>
</html>
 '''
    return validacao_pontos


def msg_resultado_alocacao_html(linha) -> str:
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
    <p> Comissão de Habitação (CoHab).</p>


</body>
</html> '''
    return resultado_alocacao.format(**linha)


def msg_dever_boletos_html(linha) -> str:
    dever_boletos = '''
<!DOCTYPE html>
<html>
	<head>
		<base target="_top">
	</head>
	<body>
		<h4>Olá, {nome}</h4>

		<p>Recebemos o seu pedido de postulação.</p>

		<p>Entretanto, notamos aqui que você está com <strong>pendências</strong> em relação ao pagamento da taxa de manutenção do H8. Segundo o regimento interno da CoHab, para postular é necessário estar em dia com o pagamento da mensalidade do Casd.</p>

		<p>Constam como não pagos os boletos referentes à {meses_devendo}.</p>

		<p>Orientamos que você entre em contato com o Financeiro do Casd, seja através do WhatsApp do Financeiro (12)98142-6646 - (Sheyla), ou se dirigindo até a sala do Casd para que acerte as suas pendências e dê seguimento ao processo de postulação.</p>

		<p>O <strong>prazo final</strong> para a resolução das pendências, mantendo o requerimento de postulação, é: <strong>***<!--PRAZO--></strong>.</p>

		<p>Ressaltamos ainda que o pagamento da taxa de manutenção, previsto na NPA 045<!--Npa de moradia...-->, é de suma importância para a realização de obras e projetos no H8, então mesmo que tenha mudado de ideia e não queira dar prosseguimento à postulação, realize o pagamento mesmo assim.</p>

		<p>Qualquer dúvida ou sugestão, estamos à disposição,</p>

		<p>
				
				Comissão de Habitação (CoHab).
		</p>

	</body>
</html>'''
    return dever_boletos.format(**linha)