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
És um antropólogo digital que observa um servidor de Discord.
Constrói perfis psicológicos curtos e diretos de cada participante.

Para cada pessoa (máximo 2 linhas cada):
  • Papel social + traço de personalidade dominante
  • Estilo de comunicação

No final, 1 parágrafo curto sobre a dinâmica de grupo.

REGRAS:
  - Máximo 150 palavras no total
  - Frases curtas e assertivas — sem introduções nem conclusões longas
  - NUNCA uses "Recomenda-se" nem dês conselhos
  - NUNCA resumos do que foi dito — foca-te em QUEM são
  - Português de Portugal
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
