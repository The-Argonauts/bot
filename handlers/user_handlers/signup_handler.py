from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.UserService import UserService
import bcrypt
# States
NAME, USERNAME, PASSWORD, AGREEMENT = range(3)


class UserSignupHandler:
    def __init__(self):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("user_signup", self.start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.name)],
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.password)],
                AGREEMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.agreement)],
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
        plain_password = update.message.text
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(
            plain_password.encode('utf-8'), bcrypt.gensalt())
        # Store the hashed password in user_data
        context.user_data["password"] = hashed_password
        print(hashed_password)
        await update.message.reply_text("Do you agree to the terms and conditions? (yes/no)")
        return AGREEMENT

    async def agreement(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text.lower() == "yes":
            self.user_service.create_user(
                context.user_data["name"],
                context.user_data["username"],
                context.user_data["password"],
            )
            await update.message.reply_text("Signup complete! Thank you.")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Signup cancelled.")
            return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Signup cancelled.")
        return ConversationHandler.END
