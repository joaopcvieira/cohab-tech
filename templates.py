dever_boletos = '''<!DOCTYPE html>
<html>
	<head>
		<base target="_top">
	</head>
	<body>
		<h4>Olá, {NOME}</h4>

		<p>No tocante ao corrente processo de postulação, recebemos o seu pedido de postulação referente às vagas {VAGAS}<!-- $vagas, talvez listadas ... usar um concat e show -->.</p>

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