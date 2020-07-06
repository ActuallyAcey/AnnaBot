import requests
from func_timeout import func_set_timeout

#pylint: disable=relative-beyond-top-level
from . import bot_config

@func_set_timeout(5)
def get_rasa_response(user_message: str, user_id: str):
    
    print(user_message)
    user_message = user_message.replace("<@!726886125440073738>", "")
    user_message = user_message.replace("<@726886125440073738>", "")
    print(user_message)
    
    url = bot_config.RASA_URL
    data = {"sender": str(user_id), "message": user_message}

    responses = []

    try:
        response_data = requests.post(url, json=data).json()    
        responses = [r["text"] for r in response_data]
    
    except:
        responses = ["Sorry, I'm not available at the moment because of some issues. Please let Acey know. Or don't, let me have the day off."]
    return responses