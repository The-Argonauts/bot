from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


class StartHandler:
    def __init__(self):
        self.handler = CommandHandler("start", self.start)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        image_path = r'assets/welcome.png'
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'))

        await update.message.reply_text(
            "Welcome to the Argonauts bot! Check out our website:\n"
            "Our guide for commands is shown above"
            "https://theargonauts.vercel.app\n\n"
            "Commands:\n"
            "/user_signup - Register as a user\n"
            "/user_login - Login as a user\n"
            "/business_signup - Register as a business\n"
            "/business_login - Login as a business"
        )
