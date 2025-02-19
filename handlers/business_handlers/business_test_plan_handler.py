from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService
from services.TestPlanService import TestPlanService
from services.UserService import UserService

PLAN_ID = range(1)


class BusinessTestPlanHandler:
    def __init__(self, business_service: BusinessService, user_service: UserService, testplan_service: TestPlanService, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("my_test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.userService = user_service
        self.testPlanService = testplan_service
        self.authorization = authorization
        self.businessService = business_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        try:
            if not self.authorization.authorize_business(str(update.effective_user.id)):
                await update.message.reply_text("You need to log in to the business portal first.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END

        business_test_plans = self.businessService.get_business_testplans(
            self.authorization.get_business_id(
                str(update.effective_user.id)))

        context.user_data["business_test_plans"] = business_test_plans

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
        await update.message.reply_text("Please enter Plan Id to view feedbacks.")
        return PLAN_ID

    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["plan_id"] = update.message.text

        business_testplan_ids = [str(test_plan.id) for test_plan in context.user_data["business_test_plans"]]

        if context.user_data["plan_id"] not in business_testplan_ids:
            await update.message.reply_text("Invalid Test Plan ID.")
            return PLAN_ID

        feedbacks = self.testPlanService.get_feedback(
            context.user_data["plan_id"])

        if not feedbacks:
            await update.message.reply_text("No feedbacks for this test plan is available.")
            return ConversationHandler.END

        for feedback in feedbacks:
            user = self.userService.get_user(feedback.user_id)
            message = (
                f"Name: {user.name}\n"
                f"Feedback: {feedback.content}"
            )
            await update.message.reply_text(message)
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Operation cancelled.")
        return ConversationHandler.END
