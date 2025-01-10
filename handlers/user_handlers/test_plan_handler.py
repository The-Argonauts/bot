from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from services.TestPlanService import TestPlanService
from services.UserService import UserService
from filters.Authorization import Authorization

PLAN_ID, APPLY = range(2)

class TestPlanHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("test_plans", self.start)],
            states={
                PLAN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_id)],
                APPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.apply_for_plan)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.testPlanService = TestPlanService()
        self.userSevice = UserService()
        self.authorization = authorization

        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        test_plans = self.testPlanService.get_all_testplans()

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

        await update.message.reply_text("Please enter Plan Id.")
        return PLAN_ID
        

    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        plan_id = update.message.text.strip()
        context.user_data["id"] = plan_id

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
            await update.message.reply_text("If you want to apply for this Test, please enter yes and if you don't want to apply for this enter No.")
            return APPLY
        else:
            await update.message.reply_text("Invalid Test Plan ID. Please enter a valid ID.")
            return PLAN_ID

        # return ConversationHandler.END   


    async def apply_for_plan(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        response = update.message.text.strip().lower()

        if response == "yes":
            print(update.effective_user.id)
            user_id = self.authorization.get_user_id(str(update.effective_user.id))
            test_plan_id = context.user_data["id"]
            self.userSevice.sign_up_for_testplan(user_id, test_plan_id)

            await update.message.reply_text("You have applied for this test plan.")
            return ConversationHandler.END
        elif response == "no":
            await update.message.reply_text("Please enter another Plan Id to view.")
            return PLAN_ID
        else:
            await update.message.reply_text("Please reply with 'Yes' or 'No'.")
            return APPLY


    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Test plans cancelled.")
        return ConversationHandler.END