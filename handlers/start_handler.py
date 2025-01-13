from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


class StartHandler:
    def __init__(self):
        self.handler = CommandHandler("start", self.start)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        gif_path = 'G:\AUT\Term7\Software\\bot\\asset\welcome-1.mp4'
        await context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_path)
        await update.message.reply_text(
            """Welcome to the Argonauts bot! Checkout our Website \n
            https://theargonauts.vercel.app/\n
            Use /user_signup to start the registration process for the user section.\n
            Use /user_login to start the login process for the user section.\n\n
            Use /business_signup to start the registration process for the business section.\n
            Use /business_login to start the login process for the business section."""
        )
