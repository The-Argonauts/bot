from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.UserService import UserService
# States
NAME, USERNAME, PASSWORD = range(3)


class UserSignupHandler:
    def __init__(self):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("user_signup", self.start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.name)],
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.password)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.user_service = UserService()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Please enter your name.")
        return NAME

    async def name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["name"] = update.message.text
        await update.message.reply_text("Please enter your username.")
        return USERNAME

    async def username(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["username"] = update.message.text
        await update.message.reply_text("Please enter your password.")
        return PASSWORD

    async def password(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["password"] = update.message.text
        await update.message.reply_text("Signup complete! Thank you.")

        self.user_service.create_user(
            context.user_data["name"],
            context.user_data["username"],
            context.user_data["password"],
        )

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Signup cancelled.")
        return ConversationHandler.END
