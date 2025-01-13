from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.TestPlanService import TestPlanService
from services.UserService import UserService
from filters.Authorization import Authorization
from datetime import datetime

PLAN_ID, FEEDBACK = range(2)


class ActiveTestPlanHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("active_test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
                FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.give_feedback)],

            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.testPlanService = TestPlanService()
        self.authorization = authorization
        self.userService = UserService()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if not self.authorization.authorize_user(str(update.effective_user.id)):
            await update.message.reply_text("You need to log in to the user portal first.")
            return ConversationHandler.END

        test_plans = self.userService.get_user_testplans(
            self.authorization.get_user_id(str(update.effective_user.id)))

        current_date = datetime.now().date()
        active_plans = [
            test_plan for test_plan in test_plans
            if test_plan.start_date <= current_date and test_plan.end_date >= current_date
        ]

        if not active_plans:
            await update.message.reply_text("There are no active test plans available.")
        else:
            for test_plan in active_plans:
                message = (
                    f"Test Plan ID: {test_plan.id}\n"
                    f"Name: {test_plan.name}\n"
                    f"Start Date: {test_plan.start_date}\n"
                    f"End Date: {test_plan.end_date}"
                )
            await update.message.reply_text(message)
        await update.message.reply_text("Please enter the Test Plan ID you want to provide feedback for.")
        context.user_data['active_plans'] = active_plans

        return PLAN_ID

    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data['plan_id'] = update.message.text

        await update.message.reply_text("Please provide your feedback for the selected Test Plan.")
        return FEEDBACK

    async def give_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data['feedback'] = update.message.text
        user_id = self.authorization.get_user_id(
            str(update.effective_user.id))

        self.userService.create_feedback(
            user_id, context.user_data['plan_id'], context.user_data['feedback'])

        await update.message.reply_text("Thank you for your feedback")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Active test plans cancelled.")
        return ConversationHandler.END
