from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService


class BusinessProfileHandler:
    def __init__(self, authorization: Authorization):
        self.handlers = [
            CommandHandler("show_business_profile", self.start),
            CommandHandler("cancel", self.cancel),
        ]
        self.business_service = BusinessService()
        self.authorization = authorization
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if not self.authorization.authorize_business(str(update.effective_user.id)):
                await update.message.reply_text("You need to login as a business first.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END
        business = self.business_service.get_business(self.authorization.get_business_id(str(update.effective_user.id)))
        message = (
            f"Name: {business.name}\n"
            f"Username: {business.username}\n"
        )
        await update.message.reply_text(message)
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Welecome to home.")
        return ConversationHandler.END

        
