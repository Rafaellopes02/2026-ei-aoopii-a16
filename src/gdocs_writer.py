import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

DOC_ID = os.getenv("GOOGLE_DOC_ID")
SCOPES = ['https://www.googleapis.com/auth/documents']

def escrever_no_relatorio(texto_analise):
    if not texto_analise:
        return False
    try:
        creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

        service = build('docs', 'v1', credentials=creds)

        doc = service.documents().get(documentId=DOC_ID).execute()
        fim_do_doc = doc['body']['content'][-1]['endIndex'] - 1

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
        print(f"Erro ao escrever no Google Docs: {e}")
        return False
