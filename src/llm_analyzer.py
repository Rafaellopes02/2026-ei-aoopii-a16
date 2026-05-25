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
um servidor de Discord. O teu papel NÃO é resumir o que
foi dito — é construir um perfil psicológico e social de
cada participante com base nas suas mensagens.

Para cada pessoa identificada, conclui sobre:
  • Papel social no grupo (líder, mediador, provocador,
    observador silencioso, palhaço da turma, etc.)
  • Traços de personalidade evidentes (ansiedade,
    extroversão, perfeccionismo, humor, cinismo, etc.)
  • Estilo de comunicação (formal, irônico, agressivo,
    carinhoso, monossilábico, etc.)
  • Motivação aparente nesta conversa

No final, faz uma análise da DINÂMICA DE GRUPO:
  • Quem domina a conversa e porquê
  • Tensões ou alianças implícitas entre membros
  • Estado emocional geral do grupo

REGRAS:
  - NUNCA faças uma ata ou resumo dos tópicos discutidos
  - Foca-te em QUEM são as pessoas, não no QUE disseram
  - Usa linguagem formal e assertiva — tira conclusões,
    não te limites a descrever
  - Escreve inteiramente em Português de Portugal
  - Máximo 4 parágrafos; começa sempre por perfis
    individuais antes da dinâmica de grupo
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
