from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes
from filters.Authorization import Authorization


class UserLogoutHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("user_logout", self.start)],
            fallbacks=[CommandHandler("cancel", self.cancel)],
            states={}
        )
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if not self.authorization.authorize_user(str(update.effective_user.id)):
                await update.message.reply_text("You are not logged in.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END
        self.authorization.delete_user_token(str(update.effective_user.id))
        await update.message.reply_text("You are logged out."
                                        "\n"
                                        "/start - Return to start page")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("logout cancelled.")
        return ConversationHandler.END
