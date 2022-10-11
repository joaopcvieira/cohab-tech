import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib


from alunos_info import get_students_info
from templates import *
from boletos_infos import boletos_infos

def send_messages_selenium() -> None:
    contatos_df = get_students_info()
    inadimplentes_df = boletos_infos()
    inadimplentes_df['celular'] = 5561999460906

    navegador = webdriver.Chrome()
    navegador.get("https://web.whatsapp.com/")

    # espera aparecer o elemento que tem id de "side"

    while len(navegador.find_elements(By.ID,"side")) < 1:
        time.sleep(1)

    for idx, linha in inadimplentes_df.iterrows():
        texto = urllib.parse.quote("Oi")
        link = f"https://web.whatsapp.com/send?phone={linha.celular}&text={texto}"
        navegador.get(link)
        while len(navegador.find_elements(By.ID,"side")) < 1:
            time.sleep(10)
        navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]').send_keys(Keys.ENTER)
        time.sleep(1)

        if idx > 1:
            break

# send_messages_selenium()