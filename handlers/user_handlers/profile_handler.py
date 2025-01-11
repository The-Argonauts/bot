from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.UserService import UserService

HOME, EDITE = range(2)

class ProfileHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("show_profile", self.start)],
            states={
                HOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.home)],
                # EDITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.edite)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.user_service = UserService()
        self.authorization = authorization
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if not self.authorization.authorize_user(str(update.effective_user.id)):
            await update.message.reply_text("You need to login as a user first.")
            return ConversationHandler.END
        
        user = self.user_service.get_user(self.authorization.get_user_id(str(update.effective_user.id)))
        message = (
            f"Name: {user.name}\n"
            f"Username: {user.username}\n"
            f"Phone number: {user.phone_number}\n"
            f"email: {user.email}\n"
            f"password: {user.password}"
        )
        await update.message.reply_text(message)

    async def home(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("welcome to home")
        return ConversationHandler.END
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("testplan creation cancelled.")
        return ConversationHandler.END

        
