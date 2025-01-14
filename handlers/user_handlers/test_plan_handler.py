from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from filters.Authorization import Authorization
from services.UserService import UserService
from services.TestPlanService import TestPlanService
from utilities.gemini import Gemini

PLAN_ID, SUGGESTION, USER_INFORMATION, APPLY = range(4)


class TestPlanHandler:
    def __init__(self, authorization: Authorization, gemini:Gemini):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
                SUGGESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.suggest_preparation)],
                USER_INFORMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.user_information)],
                APPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.apply_for_plan)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self.user_service = UserService()
        self.testplan_service = TestPlanService(gemini)
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if not self.authorization.authorize_user(str(update.effective_user.id)):
                await update.message.reply_text("You need to log in to the user portal first.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END

        test_plans = self.testplan_service.get_all_testplans()

        if not test_plans:
            await update.message.reply_text("No test plans available.")
            return ConversationHandler.END

        for test in test_plans:
            message = (
                f"Test Plan ID: {test.id}\n"
                f"Name: {test.name}\n"
                f"Start Date: {test.start_date}\n"
                f"End Date: {test.end_date}"
            )
            await update.message.reply_text(message)

        await update.message.reply_text("Please enter Test Plan Id.")
        return PLAN_ID

    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["test_plan_id"] = update.message.text.strip()

        test_plans = self.testplan_service.get_all_testplans()
        selected_test_plan = next((test for test in test_plans if str(
            test.id) == context.user_data["test_plan_id"]), None)

        if selected_test_plan:
            message = (
                f"Test Plan ID: {selected_test_plan.id}\n"
                f"Name: {selected_test_plan.name}\n"
                f"Description: {selected_test_plan.description}\n"
                f"Start Date: {selected_test_plan.start_date}\n"
                f"End Date: {selected_test_plan.end_date}"
            )
            await update.message.reply_text(message)
            await update.message.reply_text("Do you want any suggestions for preparation? (yes, no)")
            return SUGGESTION

        else:
            await update.message.reply_text("Invalid Test Plan ID. Please enter a valid ID.")
            return PLAN_ID
        # return ConversationHandler.END


    async def suggest_preparation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        response = update.message.text.strip().lower()
        if response == "yes":
            await update.message.reply_text("Please provide your information about your skills, experience, certifications, and technical proficiency related to this test plan.")
            return USER_INFORMATION

        if response == "no":
            await update.message.reply_text("Do you want to apply for this test plan? (yes, no)")
            return APPLY
        else:
            await update.message.reply_text("Please reply with 'Yes' or 'No'.")
            return SUGGESTION

    async def user_information(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_information = update.message.text.strip()
        test_plan_id = context.user_data["test_plan_id"]
        test_plan_information = self.testplan_service.get_description(test_plan_id)
        await update.message.reply_text("Please wait while we generate suggestions for you.")
        suggestions = self.testplan_service.generate_suggestions(test_plan_information, user_information)
        if len(suggestions) > 4096:
            for i in range(0, len(suggestions), 4096):
                await update.message.reply_text(suggestions[i:i+4096])
        else:
            await update.message.reply_text(suggestions)
        await update.message.reply_text("Do you want to apply for this test plan? (yes, no)")
        return APPLY

    async def apply_for_plan(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        response = update.message.text.strip().lower()

        if response == "yes":
            user_id = self.authorization.get_user_id(
                str(update.effective_user.id))
            test_plan_id = context.user_data["test_plan_id"]
            self.user_service.sign_up_for_testplan(user_id, test_plan_id)

            await update.message.reply_text("You have applied for this test plan.\n"
                                            "\n"
                                            "Commands:\n"
                                            "/active_test_plans - show active test plans")

            return ConversationHandler.END
        elif response == "no":
            await update.message.reply_text("Please enter another Test Plan Id to view.")
            return PLAN_ID
        else:
            await update.message.reply_text("Please reply with 'Yes' or 'No'.")
            return APPLY

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Test plans cancelled.")
        return ConversationHandler.END
