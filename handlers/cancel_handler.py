from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


class CancelHandler:
    def __init__(self):
        self.handler = CommandHandler("cancel", self.cancel)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Cancelled.")
