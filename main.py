from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openai
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv

load_dotenv()

# chave do ambiente
openai.api_key = os.environ.get("OPENAI_API_KEY")

options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)

print("✅ passou aqui")

# popup 
def mostrar_popup(pergunta, resposta):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo("Resposta da IA", f"Pergunta:\n{pergunta}\n\nResposta: {resposta}")
    root.destroy()

print("✅ passou aqui 2")

def processar_questao():
    try:
        print(" Tentando encontrar a pergunta e as alternativas...")
        pergunta = driver.find_element(By.CLASS_NAME, "qtext").text
        alternativas = driver.find_elements(By.CSS_SELECTOR, "div.answer div label")
        
        if pergunta.strip() and alternativas:
            print("Pergunta e alternativas encontradas. Enviando para a IA.")
        else:
            print("Pergunta ou alternativas não encontradas. Verificando novamente...")
            return
            
        lista_alternativas = [alt.text for alt in alternativas]

        prompt = f"""
        Você é um assistente de IA focado em responder a perguntas de múltipla escolha com alta precisão.
        Pergunta: {pergunta}
        Alternativas:
        A) {lista_alternativas[0]}
        B) {lista_alternativas[1]}
        C) {lista_alternativas[2]}
        D) {lista_alternativas[3]}

        Instrução: Primeiro, pense passo a passo sobre a pergunta e qual das alternativas é a mais provável. 
        Depois de chegar a uma conclusão, responda apenas com a letra da alternativa correta.
        """

        resposta = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        resposta_ia = resposta.choices[0].message.content.strip()
        mostrar_popup(pergunta, resposta_ia)

    except Exception as e:
        print(f" Erro ao processar questão: {e}")

print("✅ passou aqui 3")

# Loop
ultima_pergunta = ""
while True:
    try:
        atual = driver.find_element(By.CLASS_NAME, "qtext").text
        if atual != ultima_pergunta and atual.strip() != "":
            ultima_pergunta = atual
            print(" Nova pergunta detectada! Processando...")
            processar_questao()
    except Exception:
        time.sleep(2)
