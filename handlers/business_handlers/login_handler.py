from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService
# States
USERNAME, PASSWORD = range(2)


class BusinessLoginHandler:
    def __init__(self, business_service: BusinessService, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("business_login", self.start)],
            states={
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.password)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.business_service = business_service
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if self.authorization.authorize_user(str(update.effective_user.id)):
                await update.message.reply_text("You need to logout from user account")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END
        await update.message.reply_text("Please enter your username.")
        return USERNAME

    async def username(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["username"] = update.message.text
        await update.message.reply_text("Please enter your password.")
        return PASSWORD

    async def password(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["password"] = update.message.text
        try:
            business_id = self.business_service.validate_business(
                context.user_data["username"], context.user_data["password"])
            self.authorization.store_business_token(
                str(update.effective_user.id), business_id)

            await update.message.reply_text("you logged in successfully\n"
                                            "\n"
                                            "Commands:\n"
                                            "/show_business_profile - Show my profile\n"
                                            "/create_test_plan - Create a test plan\n"
                                            "/my_test_plans - Show all my test plans\n"
                                            "/business_logout - Log out from business profile\n"
                                            )
        except ValueError:
            await update.message.reply_text("login failed")

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("login cancelled.")
        return ConversationHandler.END
