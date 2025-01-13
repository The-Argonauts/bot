from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService
from services.TestPlanService import TestPlanService

PLAN_ID, FEEDBACK = range(2)


class TestPlanHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("all_test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
                # FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.show_feedback)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.testPlanService = TestPlanService()
        self.authorization = authorization
        self.businessService = BusinessService()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if not self.authorization.authorize_business(str(update.effective_user.id)):
            await update.message.reply_text("You need to log in to the business portal first.")
            return ConversationHandler.END

        business_test_plans = self.businessService.get_business_testplans(
            self.authorization.get_business_id(
                str(update.effective_user.id)))

        for test_plan in business_test_plans:

            message = (
                f"Test Plan ID: {test_plan.id}\n"
                f"Name: {test_plan.name}\n"
                f"Start Date: {test_plan.start_date}\n"
                f"End Date: {test_plan.end_date}"
            )
            await update.message.reply_text(message)
        await update.message.reply_text("Please enter Plan Id.")
        return PLAN_ID

    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["plan_id"] = update.message.text()

        # feedbacks = self.testPlanService.get_feedbacks(
        #     context.user_data["plan_id"])

        # context.user_data["feedbacks"] = feedbacks
        # await update.message.reply_text("Displaying feedbacks for the selected test plan.")
        # return FEEDBACK

    #  async def show_feedbacks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Operation cancelled.")
        return ConversationHandler.END
