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
                # FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.give_feedback)],

            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.testPlanService = TestPlanService()
        self.authorization = authorization
        self.userService = UserService()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if not self.authorization.authorize_user(str(update.effective_user.id)):
            await update.message.reply_text("You need to login to user portal's first.")
            return ConversationHandler.END

        print("erjfioerjgiejgioerjgierjgirjgiorejgiojgiogjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")

        test_plans = self.userService.get_user_testplans(
            self.authorization.get_user_id(str(update.effective_user.id)))
        print("erjfioerjgiejgioerjgierjgirjgiorejgiojgiogjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", test_plans)
        print("erjfioerjgiejgioerjgierjgirjgiorejgiojgiogjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", type(
            test_plans))

        current_date = datetime.now().date()

        for test_plan in test_plans:

            print(
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

            if test_plan.start_date <= current_date and test_plan.end_date >= current_date:
                print("dodoodododododoododoodododoodo")
                message = (
                    f"Test Plan ID: {test_plan.id}\n"
                    f"Name: {test_plan.name}\n"
                    f"Start Date: {test_plan.start_date}\n"
                    f"End Date: {test_plan.end_date}"
                )

                await update.message.reply_text(message)

    # test_plans = self.testPlanService.get_all_testplans()

    # if not test_plans:
    #     await update.message.reply_text("No test plans available.")
    #     return ConversationHandler.END

    # for test in test_plans:
    #     message = (
    #         f"Test Plan ID: {test.id}\n"
    #         f"Name: {test.name}\n"
    #         f"Start Date: {test.start_date}\n"
    #         f"End Date: {test.end_date}"
    #     )
    #     await update.message.reply_text(message)

    #     await update.message.reply_text("Please enter Plan Id.")
    #     return PLAN_ID
        return ConversationHandler.END

    async def select_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Active test plans cancelled.")
        return ConversationHandler.END
