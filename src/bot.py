import discord
import os
from dotenv import load_dotenv
from llm_analyzer import analisar_comportamento
from gdocs_writer import escrever_no_relatorio
from keep_alive import keep_alive

# Carrega as variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurações de permissões (intents) para o bot poder ler mensagens
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Memória temporária do bot
memoria_mensagens = []
LIMITE_MENSAGENS = 5 

@client.event
async def on_ready():
    print(f'Antropólogo Digital ligado como {client.user}')

@client.event
async def on_message(message):
    global memoria_mensagens

    # Ignora mensagens enviadas pelo próprio bot
    if message.author == client.user:
        return

    # O bot apenas observa (não responde no chat)
    conteudo_formatado = f"[{message.author}]: {message.content}"
    memoria_mensagens.append(conteudo_formatado)
    print(f"Observado: {conteudo_formatado}")

    # Quando atinge o limite, processa a análise e limpa a memória
    if len(memoria_mensagens) >= LIMITE_MENSAGENS:
        print("Limite atingido. A compilar notas antropológicas...")
        
        # 1. Pede a análise ao LLM
        relatorio = analisar_comportamento(memoria_mensagens)
        
        # 2. Escreve o resultado no Google Docs
        if relatorio:
            escrever_no_relatorio(relatorio)
        
        # 3. Limpa a memória para recomeçar o ciclo
        memoria_mensagens = []

# Bloco principal de execução
if __name__ == "__main__":
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado no ficheiro .env")
    else:
        # Inicia o servidor web invisível para enganar o Render
        keep_alive()
        # Inicia o bot do Discord
        client.run(TOKEN)