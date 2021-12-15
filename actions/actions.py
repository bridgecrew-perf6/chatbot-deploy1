# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Text, List, Any, Dict

from rasa.shared.core.constants import ACTION_DEFAULT_FALLBACK_NAME
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher, CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import UserUtteranceReverted


ALLOWED_ROOMS = range(1, 5001)
ALLOWED_NUMBER_OF_TOWELS = 20
ALLOWED_TOWEL_TYPES = ['bath', 'hand', 'washcloths']

class ValidateTowelOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_towel_order_form"

    def validate_number_of_towels(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_of_towels` value."""

        if int(slot_value) > ALLOWED_NUMBER_OF_TOWELS:
            dispatcher.utter_message(text=f"Sorry we only allow an additional 20 towels per room")
            return {"number_of_towels": None}
        else:
            dispatcher.utter_message(text=f"OK! You want {slot_value} towels")
            return {"number_of_towels": slot_value}

    def validate_towel_type(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_of_towels` value."""

        if slot_value.lower() not in ALLOWED_TOWEL_TYPES:
          dispatcher.utter_message(text=f"Sorry we only have bath, hand and washcloths, please enter another towel type")
          return {"towel_type": None}
        else:
            dispatcher.utter_message(text=f"OK! You want {slot_value} towels")
            return {"towel_type": slot_value}

    def validate_room_number(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_number` value."""

        if int(slot_value) not in range(1, 5001):
            dispatcher.utter_message(text=f"That is an invalid room number can you type again?")
            return {"room_number": None}
        else:
            dispatcher.utter_message(text=f"OK! You are in room {slot_value}")
            return {"room_number": slot_value}


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return ACTION_DEFAULT_FALLBACK_NAME

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]