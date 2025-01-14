from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.UserService import UserService
# States
NAME, USERNAME, PASSWORD, EMAIL, PHONE_NUMBER, AGREEMENT = range(6)


class UserSignupHandler:
    def __init__(self, user_service: UserService,authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("user_signup", self.start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.name)],
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.username)],
                PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.phone_number)],
                EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.email)],
                AGREEMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.agreement)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.password)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.user_service = user_service
        self.authorization = authorization
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if self.authorization.authorize_user(str(update.effective_user.id)):
                await update.message.reply_text("You need to logout from user account")
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
        await update.message.reply_text("Please enter your phone number.")
        return PHONE_NUMBER

    async def phone_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        phone_number = update.message.text.strip()  # Get the phone number and strip any extra spaces.
    
        if len(phone_number) == 11 and phone_number.isdigit():
            context.user_data["phone_number"] = phone_number
            await update.message.reply_text("Please enter your E-mail.")
            return EMAIL
        else:
            await update.message.reply_text("Invalid phone number. Please enter a valid 11-digit phone number.")
            return PHONE_NUMBER


    async def email(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        email = update.message.text.strip()  

        if "@" in email:
            context.user_data["email"] = email
            await update.message.reply_text("Please enter your password.")
            return PASSWORD
        else:
            await update.message.reply_text("Invalid email address. Please enter a valid email.")
            return EMAIL

    async def password(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["password"] = update.message.text
        await update.message.reply_text("Do you agree to the terms and conditions? (yes/no)\nBy participating as a beta tester, you agree to provide feedback on the product and understand that the software may contain bugs or incomplete features. You also agree not to share any confidential information or content provided during the testing phase. Your participation is voluntary, and the developers reserve the right to terminate your access at any time.")
        return AGREEMENT

    async def agreement(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text.lower() == "yes":
            self.user_service.create_user(
                context.user_data["name"],
                context.user_data["username"],
                context.user_data["phone_number"],
                context.user_data["email"],
                context.user_data["password"],
            )
            await update.message.reply_text(
                "Signup completed! Thank you.\n\n"
                "Commands:\n"
                "/user_login - Login as a user\n"
                "/start - Home"
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text("Signup cancelled.")
            return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Signup cancelled.")
        return ConversationHandler.END
