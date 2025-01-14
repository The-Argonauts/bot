from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from filters.Authorization import Authorization
from services.BusinessService import BusinessService
# States
NAME, DESCRIPTION, END_DATE, REWARD = range(4)


class CreateTestPlanHandler:
    def __init__(self, authorization: Authorization):
        self.handler = ConversationHandler(
            entry_points=[CommandHandler("create_test_plan", self.start)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.name)],
                DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.description)],
                END_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.end_date)],
                REWARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.reward)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.business_service = BusinessService()
        self.authorization = authorization

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            if not self.authorization.authorize_business(str(update.effective_user.id)):
                await update.message.reply_text("You need to login to business portal's first.")
                return ConversationHandler.END
        except ValueError as e:
            await update.message.reply_text(str(e))
            return ConversationHandler.END

        await update.message.reply_text("Please enter your testplan name.")
        return NAME

    async def name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["name"] = update.message.text
        await update.message.reply_text("Please enter your testplan description.")
        return DESCRIPTION

    async def description(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["description"] = update.message.text
        await update.message.reply_text("Please enter how many days from toady that you want your testplan to be active.")
        return END_DATE

    async def end_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["end_date"] = update.message.text
        await update.message.reply_text("Please enter the reward for the testplan.")
        return REWARD

    async def reward(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data["reward"] = update.message.text
        business_id = self.authorization.get_business_id(
            str(update.effective_user.id))
        business = self.business_service.get_business(business_id)

        self.business_service.create_testplan(
            business=business,
            name=context.user_data["name"],
            description=context.user_data["description"],
            start_date=datetime.now(),
            end_date=datetime.now() +
            timedelta(days=int(context.user_data["end_date"])),
            reward=context.user_data["reward"],
        )

        await update.message.reply_text("Test plan created successfully."
                                        "\n"
                                        "Commands:\n"
                                        "/my_test_plans - show my test plans")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("test plan creation cancelled.")
        return ConversationHandler.END
