from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.UserService import UserService
# States
USERNAME, PASSWORD = range(2)


class UserLoginHandler:
    def __init__(self, authorization: Authorization):

        self.handler = ConversationHandler(
            entry_points=[CommandHandler("user_login", self.start)],
            states={
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.password)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.user_service = UserService()
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Please enter your username.")
        return USERNAME

    async def username(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["username"] = update.message.text
        await update.message.reply_text("Please enter your password.")
        return PASSWORD

    async def password(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["password"] = update.message.text
        try:
            user_id = self.user_service.validate_user(context.user_data["username"], context.user_data["password"])
            self.authorization.store_user_token(str(update.effective_user.id), user_id)

            await update.message.reply_text("you logged in successfully")
        except ValueError:
            await update.message.reply_text("login failed")

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("login cancelled.")
        return ConversationHandler.END
