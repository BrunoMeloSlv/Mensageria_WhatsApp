import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib

# Carregar contatos do arquivo Excel
contatos = pd.read_excel('Downloads/Python para análise de dados (respostas).xlsx',sheet_name="Respostas ao formulário 1")
contatos.head()

# Inicializar o WebDriver
navegador = webdriver.Chrome()
navegador.get('https://web.whatsapp.com/')

# Aguardar o login manual no WhatsApp Web
WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.ID, "side")))

# Loop para enviar mensagem a cada contato
for i, contato in contatos.iterrows():
    try:
        pessoa = contato["Nome"]
        numero = contato["Telefone com DDD"]
        mensagem = "😊 Só passando para lembrar que hoje temos aula ao vivo no YouTube sobre Python. Espero você lá! 🚀🖥️"
        texto = urllib.parse.quote(f'Oi {pessoa}! {mensagem}')
        link = f'https://web.whatsapp.com/send?phone={numero}&text={texto}'
        navegador.get(link)
        
        # Aguardar o carregamento da página
        WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')))
        
        input_box = navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')
        input_box.send_keys(Keys.ENTER)
        
        # Aguardar um tempo para a mensagem ser enviada antes de passar para o próximo contato
        time.sleep(2)
        
    except Exception as e:
        print(f"Erro ao enviar mensagem para {pessoa} ({numero}): {e}")
        continue

# Fechar o navegador após o envio das mensagens
navegador.quit()
