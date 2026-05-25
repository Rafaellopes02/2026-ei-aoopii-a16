from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def analisar_comportamento(historico_mensagens, contexto_anterior=""):
    if not historico_mensagens:
        return "Não há dados suficientes para análise."

    texto_contexto = "\n".join(historico_mensagens)

    contexto_str = ""
    if contexto_anterior:
        contexto_str = f"""
OBSERVAÇÕES DO CICLO ANTERIOR (para continuidade):
{contexto_anterior}

---
"""

    prompt_sistema = """
És um antropólogo digital e psicólogo social que observa
um servidor de Discord.

Para cada participante identificado (3 a 4 linhas cada):
  • Papel social no grupo (líder, mediador, provocador, etc.)
  • Traços de personalidade evidentes
  • Estilo de comunicação
  • Motivação aparente nesta conversa

No final, 2 parágrafos curtos sobre a dinâmica de grupo:
  • Quem domina e porquê
  • Tensões ou alianças implícitas e estado emocional do grupo

REGRAS:
  - Entre 200 a 300 palavras no total
  - Frases diretas e assertivas — tira conclusões, não descreves
  - NUNCA faças resumo do que foi dito
  - NUNCA uses "Recomenda-se" nem dês conselhos
  - Foca-te em QUEM são as pessoas, não no QUE disseram
  - Escreve inteiramente em Português de Portugal
"""
    try:
        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {
                    "role": "user",
                    "content": (
                        f"{contexto_str}"
                        f"Analisa as seguintes mensagens e constrói perfis "
                        f"psicológicos e sociais de cada participante. "
                        f"Não summarizes — conclui:\n\n{texto_contexto}"
                    )
                }
            ],
            extra_headers={
                "HTTP-Referer": "https://github.com",
                "X-Title": "Discord Anthropologist IPVC",
            }
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"[Safety Warning] Erro no processamento do LLM: {e}")
        return None
