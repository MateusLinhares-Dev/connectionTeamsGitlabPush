from fastapi import FastAPI, Request, HTTPException
from core.webhook_conector import GitLabPushEvent, GitlabPushPayload
from validation.valida_trigger import validate_trigger_permission
from connection.webhook_teams import post_message_to_teams
import time
import os
from dotenv import load_dotenv
from pathlib import Path

app = FastAPI()

#load Environment Variables
enviroment_path = Path('path/to/.env')
load_dotenv(dotenv_path=enviroment_path)

USER_AGENT = os.getenv('USER_AGENT')


#Route URL webhook
@app.post("/webhook", status_code=200)
async def gitlab_webhook(payload: GitlabPushPayload, request: Request):
    #verifica se o usuário tem permissão de enviar os dados
    user_agent = request.headers.get(USER_AGENT, 'Undefined')
    validate_user = validate_trigger_permission(user_agent)

    if validate_user:
        handler = GitLabPushEvent(payload=payload)
        response = handler.process_push_event()

        #Espera 1 segundo para continuar a execução
        time.sleep(1)
        url = response['url_doc']

        #Processa a mensagem para ser encaminhado
        response = post_message_to_teams(url)  
             
        #Retorna status da comunicação
        return response
    else: 
        raise HTTPException(status_code=400, detail='Você não tem permissão de acesso')
