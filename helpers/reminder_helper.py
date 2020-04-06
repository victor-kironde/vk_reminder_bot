from datetime import datetime
from jsonpickle.unpickler import Unpickler
from botbuilder.core import TurnContext, MessageFactory
import asyncio


class ReminderHelper:
    @staticmethod
    async def remind_user(turn_context: TurnContext, storage):
        while True:
            try:

                now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
                query = f"select * from c where CONTAINS(c.id, 'Reminder') and CONTAINS(c.document.time, '{now}')"
                print(query)
                store_items =list(storage.client.QueryItems("dbs/w1hKAA==/colls/w1hKAJ-o+vY=/", query))

                ReminderLog = sorted([Unpickler().restore(item["document"]) for item in store_items])
                if len(ReminderLog)>0:
                    for reminder in ReminderLog:
                        await turn_context.send_activity(MessageFactory.text(reminder))
                await asyncio.sleep(1)
            except Exception as e:
                print("Exception occured in remind_user: ", str(e))