from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConvertTemperature(Action):

    def name(self) -> Text:
        return "action_convert_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try: 
            data = tracker.latest_message['entities'][0]["additional_info"]
        
        except: 
            data = dispatcher.utter_message("No.")
            return[]

        
        unit = None
        value = data["value"]

        if "unit" in data:
            print("Found data.")
            unit = data["unit"]

            if unit == "celsius":
                print("Found Celsius.")
                converted_value = (value * 9/5) + 32
                response = f"**{value}°C** is **{converted_value}°F**."
                dispatcher.utter_message(response)
            
            elif unit == "fahrenheit":
                print("Found Fahrenheit.")
                converted_value = (value - 32) * 5/9
                response = f"**{value}°C** is **{converted_value}°F**."
                dispatcher.utter_message(response)

        else:
            dispatcher.utter_message("Sorry, I know you're trying to convert temperatures, but I can't figure out the specifics. Try something like `What's 5C in F?` or `convert 34 farenheit to celsius`.")

        print(data)
        return []
