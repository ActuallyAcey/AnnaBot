from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConvertTemperature(Action):

    def name(self) -> Text:
        return "action_convert_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = tracker.latest_message['entities'][0]["additional_info"]
        print(data)
        return []
