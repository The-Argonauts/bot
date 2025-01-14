from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService
# States
NAME, USERNAME, PASSWORD, AGREEMENT = range(4)


class BusinessSignupHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("business_signup", self.start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.name)],
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.password)],
                AGREEMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.agreement)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.business_service = BusinessService()
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if self.authorization.authorize_business(str(update.effective_user.id)):
                await update.message.reply_text("You need to logout from your business account")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END
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
        await update.message.reply_text("Do you agree to the terms and conditions? (yes/no)\nBy using our platform to connect with beta testers, you agree to provide products that are ready for testing and accept feedback from users. You acknowledge that testers may encounter bugs or issues, and you will not hold them liable for any unintended outcomes during the testing process. We reserve the right to remove or suspend any testing activity that violates our guidelines or policies.")
        return AGREEMENT

    async def agreement(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text.lower() == "yes":
            self.business_service.create_business(
                context.user_data["name"],
                context.user_data["username"],
                context.user_data["password"],
            )
            await update.message.reply_text("Signup complete! Thank you.\n"
                                            "\n"
                                            "Commands:\n"
                                            "/business_login - Login as a business\n"
                                            "/start - Home"
                                            )
            return ConversationHandler.END
        else:
            await update.message.reply_text("Signup cancelled.")
            return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Signup cancelled.")
        return ConversationHandler.END
