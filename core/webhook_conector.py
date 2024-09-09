from pydantic import BaseModel
import re
from fastapi import HTTPException
from typing import List

# Modelo de dados para o payload do GitLab
class CommitAuthor(BaseModel):
    name: str
    email: str

class Repository(BaseModel):
    name: str
    url: str
    description: str
    homepage: str
    git_http_url: str
    git_ssh_url: str
    visibility_level: int

class Commit(BaseModel):
    id: str
    message: str
    timestamp: str
    url: str
    author: CommitAuthor
    added: List[str]
    modified: List[str]
    removed: List[str]

class GitlabPushPayload(BaseModel):
    object_kind: str
    event_name: str
    before: str
    after: str
    ref: str
    user_name: str
    commits: List[Commit]
    repository: Repository
    

class GitLabPushEvent:
    def __init__(self, payload: GitlabPushPayload) -> GitlabPushPayload:
        self.payload = payload

    def process_push_event(self):
        # Verifica se o evento é de push
        if self.payload.object_kind == "push":
            return self.handle_push_event()
        else:
            raise HTTPException(status_code=400, detail="Evento desconhecido")
    
    def handle_push_event(self):
        commits = self.payload.commits
        # timestamp = [getattr(commit, 'timestamp') for commit in commits]
        # print(timestamp)

        
        commit_event = []
        found_new_conector = False
        for commit in commits:
            message = getattr(commit, 'message').lower()
            if 'create conector' in message:
                commit_event.append(message)
                found_new_conector = True
            else:
                commit_event.append('Nenhum novo conector foi encontrado')

        if not found_new_conector:
            raise HTTPException(status_code=400, detail='Nenhum conector encontrado')


        # Extrai a url da documentação
        pattern = r"url=https:\/\/gitlab\.softexpert\.network\/on-demand-development\/odd-conectores\/src\/([^/]+)$"
        url = ''
        for c in commit_event:
            match = re.search(pattern, c)
            if match:
                url += match.group()

        #verifica se encontrou a url da documentação, caso não mostre um erro
        if url != '':
            url_split = url.split('=')[1]
        else:
            raise HTTPException(status_code=400, detail='Está faltando a url da documentação')
        
        return {
            "commit_messages": commit_event,
            "url_doc": url_split,
            }

if __name__ == "__main__":
    print('Iniciou o módulo: ', __name__)