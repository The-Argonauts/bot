from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService
from services.TestPlanService import TestPlanService
from services.UserService import UserService

PLAN_ID = range(1)


class BusinessTestPlanHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("signed_up_testusers", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.userService = UserService()
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

        if not business_test_plans:
            await update.message.reply_text("No test plans available.")
            return ConversationHandler.END

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
        context.user_data["plan_id"] = update.message.text

        all_users = self.testPlanService.get_users(
            context.user_data["plan_id"])

        if not all_users:
            await update.message.reply_text("There are no users for this test plan.")
            return ConversationHandler.END

        for user in all_users:
            user = self.userService.get_user(user.user_id)
            message = (
                f"Name: {user.name}\n"
                f"Email: {user.email}"
                f"Phone Number: {user.phone_number}"
            )
            await update.message.reply_text(message)
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Operation cancelled.")
        return ConversationHandler.END
