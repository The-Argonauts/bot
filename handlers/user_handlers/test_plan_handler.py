from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.TestPlanService import TestPlanService

class TestPlanHandler:
    def __init__(self):
        self.handler = CommandHandler("test_plans", self.start)
        self.testPlanService = TestPlanService()

        
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        test_plans = self.testPlanService.get_all_testplans()

        if test_plans:
            for test in test_plans:
                message = (
                    f"Test Plan ID: {test.id}\n"
                    f"Name: {test.name}\n"
                    f"Start Date: {test.start_date}\n"
                    f"End Date: {test.end_date}"
                )
                await update.message.reply_text(message)
        else:
            await update.message.reply_text("No test plans available.")