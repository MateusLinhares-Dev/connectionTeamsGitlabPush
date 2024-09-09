import requests
from fastapi import HTTPException
import json
import os
from dotenv import load_dotenv
from pathlib import Path

#load Environment Variables
enviroment_path = Path('path/to/.env')
load_dotenv(dotenv_path=enviroment_path)

URL_WEBHOOK = os.getenv('URL_WEBHOOK')

#Lógica para encaminhar mensagem no grupo do teams
def post_message_to_teams(url):

    url_webhook = URL_WEBHOOK

    headers = {
    'Content-Type': 'application/json'
    }


    payload = {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "version": "1.2",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "**🚀 Novo Conector Disponível!**",
                        "size": "Large",
                        "weight": "Bolder",
                        "color": "Good",
                        "wrap": True
                    },
                    {
                        "type": "Image",
                        "url": "https://i.ytimg.com/vi/xHbTiIv-v1s/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGEcgVihlMA8=&rs=AOn4CLDbiM7RbMrlcR0kURqhddhefE3KIg",  # Substitua com o URL da imagem que você deseja
                        "size": "Large", #Tamanho grande da imagem
                        "altText": "Logo do Conector"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Clique no link abaixo para acessar a documentação e aprender mais.",
                        "wrap": True,
                        "spacing": "Medium"
                    },
                    {
                        "type": "FactSet",
                        "facts": [
                            {
                                "title": "Versão:",
                                "value": "1.0.0"
                            },
                            {
                                "title": "Data de Lançamento:",
                                "value": "2024-09-05"
                            },
                            {
                                "title": "Autor:",
                                "value": "Equipe de Integração"
                            }
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": "Funcionalidades do Conector:",
                        "weight": "Bolder",
                        "spacing": "Medium"
                    },
                    {
                        "type": "TextBlock",
                        "text": "- Consome APIs externas\n- Faz tratamento de dados\n- Facilita integrações complexas",
                        "wrap": True
                    },
                    {
                        "type": "TextBlock",
                        "text": "Tem alguma dúvida? Entre em contato com nosso time de suporte!",
                        "spacing": "Medium",
                        "weight": "Bolder"
                    }
                ],
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "📄 Acessar Documentação",
                        "url": f"{url}"
                    },
                    {
                        "type": "Action.OpenUrl",
                        "title": "🛠 Acessar Repositório do Código",
                        "url": "https://example.com/repository"  # Substitua pelo link do repositório
                    },
                    {
                        "type": "Action.Submit",
                        "title": "❓ Enviar Feedback",
                        "data": {
                            "type": "feedback",
                            "connectorId": "12345"  # Exemplo de ID do conector
                        }
                    }
                ]
            }
        }
    ]
}



    response = requests.post(url_webhook, headers=headers, data =json.dumps(payload)) 
    
    if response.status_code == 200:
        return {"status": "Mensagem encaminhada com Sucesso, visualize no grupo do Teams"}
    else: 
        raise HTTPException(
          status_code=400, detail='Erro no envio'
        )
    
if __name__ == "__main__":
    url = 'https://softexpertjlle.webhook.office'
    response = post_message_to_teams(url=url)
    print(response)