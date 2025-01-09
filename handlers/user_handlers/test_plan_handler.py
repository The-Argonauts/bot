from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.TestPlanService import TestPlanService

PLAN_ID = range(1)

class TestPlanHandler:
    def __init__(self):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.id)],

            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.testPlanService = TestPlanService()
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
        
        await update.message.reply_text("Please enter Plan Id.")
        return PLAN_ID
        

    async def id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["id"] = update.message.text
        
        test_plans = self.testPlanService.get_all_testplans()
        selected_test_plan = next((test for test in test_plans if str(test.id) == context.user_data["id"]), None)

        if selected_test_plan:
            message = (
                f"Test Plan ID: {selected_test_plan.id}\n"
                f"Name: {selected_test_plan.name}\n"
                f"Description: {selected_test_plan.description}\n"
                f"Start Date: {selected_test_plan.start_date}\n"
                f"End Date: {selected_test_plan.end_date}"
            )
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("Invalid Test Plan ID. Please enter a valid ID.")
            return PLAN_ID

        return ConversationHandler.END    


    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Test plans cancelled.")
        return ConversationHandler.END