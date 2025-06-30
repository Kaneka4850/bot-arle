import json
import os

# Funções para carregar e salvar JSON
def carrega(nome, default):
    if os.path.exists(nome):
        with open(nome, encoding="utf-8") as f:
            return json.load(f)
    with open(nome, "w", encoding="utf-8") as f:
        json.dump(default, f, ensure_ascii=False, indent=4)
    return default

def salva(arq, data):
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Função para enviar log
async def enviar_log(guild, mensagem, view=None, canal_id=None):
    canal = guild.get_channel(canal_id)
    if canal:
        await canal.send(mensagem, view=view)
