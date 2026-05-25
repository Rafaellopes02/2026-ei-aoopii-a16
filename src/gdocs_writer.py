import os
import traceback
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

DOC_ID = os.getenv("GOOGLE_DOC_ID")
SCOPES = ['https://www.googleapis.com/auth/documents']
ultimo_erro = ""

def escrever_no_relatorio(texto_analise):
    global ultimo_erro
    print("=== A TENTAR ESCREVER NO GOOGLE DOCS ===")

    if not texto_analise:
        print("ERRO: texto_analise está vazio")
        return False

    credentials_path = '/etc/secrets/credentials.json'
    print(f"A verificar credenciais em: {credentials_path}")
    print(f"Ficheiro existe: {os.path.exists(credentials_path)}")

    if not os.path.exists(credentials_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        credentials_path = os.path.join(base_dir, 'credentials.json')
        print(f"A usar caminho local: {credentials_path}")
        print(f"Ficheiro local existe: {os.path.exists(credentials_path)}")

    try:
        print("A carregar credenciais...")
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        print("Credenciais carregadas com sucesso!")

        service = build('docs', 'v1', credentials=creds)
        print("Serviço Google Docs criado!")

        doc = service.documents().get(documentId=DOC_ID).execute()
        fim_do_doc = doc['body']['content'][-1]['endIndex'] - 1
        print(f"Documento lido, fim em índice: {fim_do_doc}")

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        requests = [{
            'insertText': {
                'location': {'index': fim_do_doc},
                'text': f"\n--- Observação: {timestamp} ---\n{texto_analise}\n"
            }
        }]
        service.documents().batchUpdate(
            documentId=DOC_ID, body={'requests': requests}).execute()
        print("Escrita no Google Docs bem sucedida!")
        return True

    except Exception as e:
        ultimo_erro = str(e)
        print(f"ERRO GOOGLE DOCS: {e}")
        traceback.print_exc()
        return False
