from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env
load_dotenv()

# Configuração específica para o OpenRouter (conforme indicado no quadro)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def analisar_comportamento(historico_mensagens):
    """
    Processamento (LLM via OpenRouter).
    Garante o 'Liveness' do agente: transforma os dados crus num relatório útil.
    """
    if not historico_mensagens:
        return "Não há dados suficientes para análise."

    # Ingestão processada
    texto_contexto = "\n".join(historico_mensagens)

    prompt_sistema = """
    És um antropólogo digital passivo que observa o comportamento humano num servidor de Discord.
    O teu objetivo é identificar padrões, tópicos recorrentes e o estado emocional geral do grupo.
    Nunca interages, apenas observas. Escreve um breve relatório formal (máximo 3 parágrafos) com as tuas conclusões.
    """

    # Safety: Bloco Try-Except para garantir que o Loop do agente não morre se a API falhar
    try:
        response = client.chat.completions.create(
            # Vamos usar um modelo gratuito e muito rápido disponível no OpenRouter
            model="openrouter/auto",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Aqui estão as conversas recentes para análise:\n\n{texto_contexto}"}
            ],
            # O OpenRouter gosta que identifiques a app (opcional, mas boa prática)
            extra_headers={
                "HTTP-Referer": "https://github.com", # Pode ser qualquer URL
                "X-Title": "Discord Anthropologist IPVC", 
            }
        )
        return response.choices[0].message.content
    
    except Exception as e:
        # Garante a 'Safety' ao não deixar o programa crashar
        print(f"[Safety Warning] Erro no processamento do LLM: {e}")
        return None