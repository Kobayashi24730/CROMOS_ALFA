import os
import sys
import time
from speech.stt import gravar_audio, transcrever_audio
from nlp.chat import chat_process
from memory.memory_acoes import acoes_disponiveis

def executar_acao(comando_ia):
    comando_ia_upper = comando_ia.upper()
    if "ACAO:" in comando_ia_upper or "ACÂO:" in comando_ia_upper:
        print(f"⚙️ Gatilho detectado {comando_ia_upper}")
        ##acao = comando_ia.split("ACAO:")[1].split("]")[0].strip()
        acao_executada = False

        for palavra_chave, comando_sistema in acoes_disponiveis.items():
            if palavra_chave in comando_ia_upper():
                print("🪟 Executando: {palavra_chave} -> {comando_sistema}.")
                os.system(comando_sistema)
                acao_executada = True
                break
        if not acao_executada:
            print("⚠️ Ação reconhecida pela CROMOS mas nao mapeada.")
        print("-" * 30)

def main():
    print("=== CROMOS ALFA INICIANDO ===")
    print("Diga 'sair' ou 'encerrar' a qualquer momento para fechar o assistente. \n")

    try:
        while True:
            gravar_audio()
            texto_ditado = transcrever_audio()
            if not texto_ditado or len(texto_ditado):
                print("❌ Não entendi o que você quis dizer.")
                time.sleep(1)
                continue
            print(f"🗣️ Você quis dizer {texto_ditado}")
            if any(palavra in texto_ditado.lower() for list_p in ['sair', 'encerrar', 'fechar assistente'] for palavra in list_p.split()):
                print("👋 Ate logo, CROMOS esta encerrando...")
                break

            print("🧠 Pensando...")
            resposta_ia = chat_process(texto_ditado)
            executar_acao(resposta_ia)
    except KeyboardInterrupt:
        print("\nEncerrando o assistente...")

if __name__ == "__main__":
    main()
