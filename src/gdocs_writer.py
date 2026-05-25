import os
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv()

DOC_ID = os.getenv("GOOGLE_DOC_ID")
SCOPES = ['https://www.googleapis.com/auth/documents']

def escrever_no_relatorio(texto_analise):
    if not texto_analise:
        return False

    try:
        # 1. Tenta o caminho padrão de segredos do Render
        credentials_path = '/etc/secrets/credentials.json'
        
        # 2. Se não existir (significa que estás no PC local), usa o ficheiro da tua pasta raiz
        if not os.path.exists(credentials_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            credentials_path = os.path.join(base_dir, 'credentials.json')

        # Carrega as credenciais com o caminho correto detetado
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        service = build('docs', 'v1', credentials=creds)

        # Lê o documento para saber o índice do fim
        doc = service.documents().get(documentId=DOC_ID).execute()
        fim_do_doc = doc['body']['content'][-1]['endIndex'] - 1

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        requests = [
            {
                'insertText': {
                    'location': {'index': fim_do_doc},
                    'text': f"\n--- Observação: {timestamp} ---\n{texto_analise}\n"
                }
            }
        ]

        service.documents().batchUpdate(
            documentId=DOC_ID, body={'requests': requests}).execute()

        print(f"Relatório adicionado ao fim do documento ({timestamp})")
        return True

    except Exception as e:
         print(f"ERRO GOOGLE DOCS DETALHADO: {e}")
    import traceback
    traceback.print_exc()
    return False
