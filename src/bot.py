import discord
import os
from dotenv import load_dotenv
from llm_analyzer import analisar_comportamento
from gdocs_writer import escrever_no_relatorio
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

memoria_mensagens = []
LIMITE_MENSAGENS = 5

# Contexto acumulado entre ciclos (memória longa do agente)
resumo_anterior = ""

@client.event
async def on_ready():
    print(f'Antropólogo Digital ligado como {client.user}')


@client.event
async def on_message(message):
    global resumo_anterior, memoria_mensagens  # <--- As duas variáveis globais aqui!

    if message.author == client.user:
        return

    conteudo_formatado = f"[{message.author.display_name}]: {message.content}"
    memoria_mensagens.append(conteudo_formatado)
    print(f"Observado: {conteudo_formatado}")

    if len(memoria_mensagens) >= LIMITE_MENSAGENS:
        # Envia um aviso no chat para saberes que ele começou a trabalhar
        await message.channel.send("🤖 *Limite atingido! A enviar dados para o Antropólogo...*")
        print("Limite atingido. A compilar notas antropológicas...")

        # Passa o contexto do ciclo anterior ao analisador
        relatorio = analisar_comportamento(
            memoria_mensagens,
            contexto_anterior=resumo_anterior
        )

        if not relatorio:
            await message.channel.send("❌ *Erro: O OpenRouter (LLM) não devolveu nenhum relatório.*")
            memoria_mensagens.clear()  # Limpa para não bloquear o bot
            return

        # Tenta escrever no Google Docs
        sucesso = escrever_no_relatorio(relatorio)

        if sucesso:
            await message.channel.send("✅ *Relatório guardado com sucesso no Google Docs!*")
            # Guarda um resumo curto para o próximo ciclo
            resumo_anterior = relatorio[:500]
            # .clear() é thread-safe
            memoria_mensagens.clear()
        else:
             import traceback
             print("ERRO DETALHADO:", traceback.format_exc())
            await message.channel.send("❌ *Erro: Falha ao gravar no Google Docs. Verifica as credenciais no Render.*")
            # Dica: Não limpamos a memória aqui para poderes tentar outra vez

if __name__ == "__main__":
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado no ficheiro .env")
    else:
        keep_alive()
        client.run(TOKEN)
