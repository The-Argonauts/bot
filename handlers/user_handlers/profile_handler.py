from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes

from filters.Authorization import Authorization
from services.UserService import UserService


class ProfileHandler:
    def __init__(self, user_service: UserService, authorization: Authorization):
        self.handlers = [
            CommandHandler("show_user_profile", self.start),
            CommandHandler("cancel", self.cancel),
        ]
        self.user_service = user_service
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if not self.authorization.authorize_user(str(update.effective_user.id)):
                await update.message.reply_text("You need to login as a user first.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END

        user = self.user_service.get_user(
            self.authorization.get_user_id(str(update.effective_user.id)))
        message = (
            f"Name: {user.name}\n"
            f"Username: {user.username}\n"
            f"Phone number: {user.phone_number}\n"
            f"email: {user.email}\n"
        )
        await update.message.reply_text(message)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Welecome to home.")
        return ConversationHandler.END
