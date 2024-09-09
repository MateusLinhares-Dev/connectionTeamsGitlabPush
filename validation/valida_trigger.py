import re
import os
from dotenv import load_dotenv
from pathlib import Path

#load Environment Variables
enviroment_path = Path('path/to/.env')
load_dotenv(dotenv_path=enviroment_path)

PATTERN_AGENT_USER = os.getenv('PATTERN_AGENT_USER')

#valida se o usuário tem permissão de usar o webhook
def validate_trigger_permission(user_agent):
    validate_user = False
    match = re.compile(PATTERN_AGENT_USER)
    pattern = re.match(match, user_agent)

    if pattern:
        validate_user = True
        return validate_user
    
    return validate_user