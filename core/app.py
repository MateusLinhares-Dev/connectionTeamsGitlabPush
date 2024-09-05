from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    status: int
    messageTeams: str

@app.post("/webhook", status_code=200, response_model=Item)
async def gitlab_webhook(request: Request, item: Item) -> Item:
    # Verifica se o evento é um push hook
    host_client = 'push hook' in request.headers.get('X-Gitlab-Event', '').lower()

    if host_client:
        payload = await request.json()
        
        # Busca a referência
        ref = payload.get('ref', "Não foi encontrado referência")
        commits = payload.get('commits')

        # Busca se há referência ao conector na mensagem do commit
        connectors_push = any("conector" in commit["message"].lower() for commit in commits)

        if connectors_push:
            # Adicione lógica específica aqui se necessário
            return item
        else:
            # Se não houver referência ao conector
            item.status = 204
            item.messageTeams = "Nenhum commit relacionado a conector encontrado."
            return item
    else: 
        # Levanta uma exceção HTTP se o evento for incorreto
        raise HTTPException(status_code=400, detail="O Evento é incorreto, use no local correto")

