import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv()

DOC_ID = os.getenv("GOOGLE_DOC_ID")
SCOPES = ['https://www.googleapis.com/auth/documents']

def escrever_no_relatorio(texto_analise):
    """
    Adiciona o texto gerado pela IA ao fim do documento Google.
    """
    if not texto_analise:
        return False

    # NOTA: Precisam do ficheiro credentials.json gerado na Google Cloud Console
    try:
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        service = build('docs', 'v1', credentials=creds)

        # Comando para inserir texto no final do documento
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1 # Insere no topo. Para inserir no fim, é preciso ler o tamanho do doc primeiro.
                    },
                    'text': f"\n--- Nova Observação ---\n{texto_analise}\n"
                }
            }
        ]

        result = service.documents().batchUpdate(
            documentId=DOC_ID, body={'requests': requests}).execute()
        
        print("Relatório atualizado com sucesso no Google Docs!")
        return True
    
    except Exception as e:
        print(f"Erro ao escrever no Google Docs: {e}")
        print("Verifiquem se têm o ficheiro credentials.json configurado corretamente.")
        return False
