import discord
import os
from dotenv import load_dotenv
from llm_analyzer import analisar_comportamento
from gdocs_writer import escrever_no_relatorio
from keep_alive import keep_alive
import traceback

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
memoria_mensagens = []
LIMITE_MENSAGENS = 5
resumo_anterior = ""

@client.event
async def on_ready():
    print(f'Antropólogo Digital ligado como {client.user}')

@client.event
async def on_message(message):
    global resumo_anterior, memoria_mensagens
    if message.author == client.user:
        return

    conteudo_formatado = f"[{message.author.display_name}]: {message.content}"
    memoria_mensagens.append(conteudo_formatado)
    print(f"Observado: {conteudo_formatado}")

    if len(memoria_mensagens) >= LIMITE_MENSAGENS:
        await message.channel.send("🤖 *Limite atingido! A enviar dados para o Antropólogo...*")
        print("Limite atingido. A compilar notas antropológicas...")

        relatorio = analisar_comportamento(
            memoria_mensagens,
            contexto_anterior=resumo_anterior
        )

        if not relatorio:
            await message.channel.send("❌ *Erro: O OpenRouter (LLM) não devolveu nenhum relatório.*")
            memoria_mensagens.clear()
            return

        sucesso = escrever_no_relatorio(relatorio)

        if sucesso:
            await message.channel.send("✅ *Relatório guardado com sucesso no Google Docs!*")
            resumo_anterior = relatorio[:500]
            memoria_mensagens.clear()
        else:
            from gdocs_writer import ultimo_erro
            await message.channel.send(f"❌ *Erro Google Docs:* `{ultimo_erro}`")
            memoria_mensagens.clear()

if __name__ == "__main__":
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado no ficheiro .env")
    else:
        keep_alive()
        client.run(TOKEN)
