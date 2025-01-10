from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.UserService import UserService


class ProfileHandler:

    def __init__(self, user_service):
        self.handler = CommandHandler("user_profile", self.show_profile)
        self.user_service = user_service
