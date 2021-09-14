from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.forms import FormAction
import random
from database_api import DatabaseAPI, CancelAPI, DetailsAPI

pick_up=str()
destination=str()
book_id=int()

class ActionSessionStart(Action):

   def name(self) -> Text:
        return "action_session_start"

   def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

       dispatcher.utter_message("Hi, I am Woody. How may I help you")
       events=[SessionStarted()]
       events.append(ActionExecuted("action_listen"))

       return events


class ActionFrom(Action):

    def name(self) -> Text:
        return "action_from"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> None:

        dispatcher.utter_message("Please mention the pick-up point")
        pick_up=tracker.latest_message['text']
        print(pick_up)

        return


class ActionTo(Action):

    def name(self) -> Text:
        return "action_to"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> None:

        dispatcher.utter_message("Please mention the destination point")
        destination=tracker.latest_message['text']
        print(destination)

        return

class ActionBooked(Action):

    def name(self) -> Text:
        return "action_booked"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> None:

        print(pick_up)
        print(destination)

        return

class ActionFormInfo(FormAction):

    def name(self) -> Text:
        return "form_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["mobile","source","arrival"]

    def slot_mappings(self) -> Dict[Text, Any]:

        return {
             "mobile": [self.from_text(intent=None), self.from_text()],
             "source": [self.from_text(intent=None), self.from_text()],
             "arrival": [self.from_text(intent=None), self.from_text()]
              }

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],) -> List[Dict]:

        global book_id
        book_id=random.randint(10000,99999)

        DatabaseAPI(book_id,tracker.get_slot('mobile'),tracker.get_slot('source'),tracker.get_slot('arrival'))
        dispatcher.utter_message(template="utter_booked",id=book_id,number=tracker.get_slot('mobile'),
                                 pick_up=tracker.get_slot('source'),
                                 destination=tracker.get_slot('arrival'))

        return []


class ActionFormCancel(FormAction):

    def name(self) -> Text:
        return "form_cancel"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["bookingid"]

    def slot_mappings(self) -> Dict[Text, Any]:

        return {
             "bookingid": [self.from_text(intent=None), self.from_text()]
              }

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],) -> List[Dict]:

        CancelAPI(tracker.get_slot('bookingid'))
        dispatcher.utter_message("Your booking has been cancelled. Have a good day")

        return []


class ActionFormDetails(FormAction):

    def name(self) -> Text:
        return "form_details"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["bookingid"]

    def slot_mappings(self) -> Dict[Text, Any]:

        return {
             "bookingid": [self.from_text(intent=None), self.from_text()]
              }

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],) -> List[Dict]:

        details=DetailsAPI(tracker.get_slot('bookingid'))
        details=str(details)
        dispatcher.utter_message("Here are your booking details: ",details)

        return []