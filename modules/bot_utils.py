import requests
import re
from func_timeout import func_set_timeout

#pylint: disable=relative-beyond-top-level
from . import bot_config

@func_set_timeout(7)
def get_rasa_response(user_message: str, user_id: str, bot_id):
    user_message = re.sub(fr"(\s|^)(<@(!|&)?{bot_id}>)(\s)?", user_message, "")
    url = bot_config.RASA_URL
    data = {"sender": str(user_id), "message": user_message}

    responses = []

    try:
        response_data = requests.post(url, json=data).json()    
        responses = [r["text"] for r in response_data]
    
    except Exception as e:
        responses = ["Sorry, I'm not available at the moment because of some issues. Please let Acey know. Or don't, let me have the day off."]
        print("FATAL ============================================")
        print(e)
    return responses


def regex_check_mention(message, id):
    return re.search(fr"(\s|^)(<@(!|&)?{id}>)(\s)?", message) is not None