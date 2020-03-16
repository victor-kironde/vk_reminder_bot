from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext, MessageFactory
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from data_models import Reminder, WelcomeUserState


class ReminderBot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise Exception(
                "[DialogBot]: Missing parameter. conversation_state is required"
            )
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
        self.user_state_accessor = self.user_state.create_property("WelcomeUserState")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)
        u_state = self.user_state_accessor.get(turn_context, WelcomeUserState)
        # print("USER STATE", u_state.__dict__)

    async def on_message_activity(self, turn_context):
        await self._welcome_user(turn_context)
        return await DialogHelper.run_dialog(
        self.dialog,
        turn_context,
        self.conversation_state.create_property("DialogState"),
        )

    async def on_members_added_activity(self, members_added, turn_context):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await self._welcome_user(turn_context)
        return await DialogHelper.run_dialog(
        self.dialog,
        turn_context,
        self.conversation_state.create_property("DialogState"),
        )


    async def _welcome_user(self, turn_context: TurnContext):
        welcome_user_state = await self.user_state_accessor.get(
    turn_context, WelcomeUserState
    )
        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True
            name = turn_context.activity.from_property.name
            await turn_context.send_activity(
                f"Hello {name}!"
            )
            await turn_context.send_activity(
                f"I'm VK-Reminder-Bot."
            )
