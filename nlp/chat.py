import ollama
from memory.pront import system_prompt
import dotenv
import os
import json

CAMINHO_HISTORICO_JSON = "memory/historico.json"
if os.path.exists(CAMINHO_HISTORICO_JSON):
    with open(CAMINHO_HISTORICO_JSON, 'r', encoding='utf-8') as arquivo:
        historico = json.load(arquivo)

def chat_process(Texto_usuario):
    global historico
    historico.append({'role': 'user', 'content': Texto_usuario})
    try:
        response = ollama.chat(model="llama3", messages=historico)
        resposta_ia = response['message']['content']
        historico.append({'role': 'assistant', 'content': resposta_ia})
        return resposta_ia
    except Exception as e:
        return f"Erro ao connectar ollama {e}"

