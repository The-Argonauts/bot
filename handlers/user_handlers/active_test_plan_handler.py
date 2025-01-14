from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.TestPlanService import TestPlanService
from services.UserService import UserService
from filters.Authorization import Authorization
from datetime import datetime

PLAN_ID, ASK_FEEDBACK, FEEDBACK = range(3)


class ActiveTestPlanHandler:
    def __init__(self, testplan_service: TestPlanService, user_service: UserService, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("active_test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
                ASK_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.ask_feedback)],
                FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.give_feedback)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.testPlanService = testplan_service
        self.authorization = authorization
        self.userService = user_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        try:
            if not self.authorization.authorize_user(str(update.effective_user.id)):
                await update.message.reply_text("You need to log in to the user portal first.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END

        test_plans = self.userService.get_user_testplans(
            self.authorization.get_user_id(str(update.effective_user.id)))

        current_date = datetime.now().date()
        active_plans = [
            test_plan for test_plan in test_plans
            if test_plan.start_date <= current_date <= test_plan.end_date
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
                context.user_data['active_plans'] = active_plans
                await update.message.reply_text("Do you want to provide feedback for the selected Test Plan? (Yes/No)")

        return ASK_FEEDBACK

    async def ask_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text.lower() == "no":
            return ConversationHandler.END
        await update.message.reply_text("Please enter the Test Plan ID you want to provide feedback for.")
        return PLAN_ID


    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data['plan_id'] = update.message.text

        plan_id = context.user_data['plan_id']
        if not plan_id.isdigit():
            await update.message.reply_text("Invalid Test Plan ID. Please enter a valid Test Plan ID.")
            return PLAN_ID

        await update.message.reply_text("Please provide your feedback for the selected Test Plan.")
        return FEEDBACK

    async def give_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data['feedback'] = update.message.text
        user_id = self.authorization.get_user_id(
            str(update.effective_user.id))

        try:
            self.userService.create_feedback(
                user_id, context.user_data['plan_id'], context.user_data['feedback'])
        except Exception as e:
            await update.message.reply_text(f"Feedback failed to submit. Please try again. {e}")
            return ConversationHandler.END

        gif_path = r'assets/reward.mp4'
        await context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_path, caption="Here is a gif for you!")
        await update.message.reply_text("Thank you for your feedback"
                                        "\n"
                                        "Commands:\n"
                                        "/active_test_plans - show active test plans \n"
                                        "/test_plans - show all test plans")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Active test plans cancelled.")
        return ConversationHandler.END
