from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


class StartHandler:
    def __init__(self):
        self.handler = CommandHandler("start", self.start)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Welcome to the bot! \n Use /user_signup to start the registration process for the user section. \n Use /business_signup to start the registration process for the business section.\n Use /user_login to start the login process for the user section.\n Use /business_login to start the login process for the business section."
        )