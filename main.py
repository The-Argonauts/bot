from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

from configs.database import SessionLocal
from configs.redis import RedisClient
from filters.Authorization import Authorization
from handlers.business_handlers.create_testplan_handler import CreateTestPlanHandler
from handlers.business_handlers.login_handler import BusinessLoginHandler
from handlers.business_handlers.logout_handler import BusinessLogoutHandler
from handlers.business_handlers.signup_handler import BusinessSignupHandler
from handlers.start_handler import StartHandler
from handlers.user_handlers.login_handler import UserLoginHandler
from handlers.user_handlers.logout_handler import UserLogoutHandler
from handlers.user_handlers.signup_handler import UserSignupHandler
from handlers.cancel_handler import CancelHandler
from handlers.user_handlers.test_plan_handler import TestPlanHandler
from handlers.user_handlers.active_test_plan_handler import ActiveTestPlanHandler
from handlers.user_handlers.profile_handler import ProfileHandler
import os
from handlers.business_handlers.business_test_plan_handler import BusinessTestPlanHandler

from handlers.business_handlers.business_profile_handler import BusinessProfileHandler
from repositories.BusinessRepository import BusinessRepository
from repositories.FeedbackRepository import FeedbackRepository
from repositories.TestPlanRepository import TestPlanRepository
from repositories.UserRepository import UserRepository
from services.BusinessService import BusinessService
from services.TestPlanService import TestPlanService
from services.UserService import UserService
from utilities.gemini import Gemini


def main():

    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    gemini_model = os.getenv('GEMINI_MODEL_NAME')
    app = ApplicationBuilder().token(token).build()
    redis_client = RedisClient()

    redis_client.connect()
    auth = Authorization(redis_client)
    gemini = Gemini(gemini_api_key, gemini_model)

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in the .env file")
    db_session = SessionLocal()

    ############################## Repository Registration ##############################
    user_repo = UserRepository(db_session)
    business_repo = BusinessRepository(db_session)
    testplan_repo = TestPlanRepository(db_session)
    feedback_repo = FeedbackRepository(db_session)

    ############################## Service Registration ##############################
    user_service = UserService(user_repo, feedback_repo, testplan_repo)
    business_service = BusinessService(business_repo)
    testplan_service = TestPlanService(testplan_repo, feedback_repo, gemini)

    ############################## Handler Registration ##############################
    start_handler = StartHandler()
    user_signup_handler = UserSignupHandler(user_service, auth)
    user_login_handler = UserLoginHandler(user_service, auth)
    user_logout_handler = UserLogoutHandler(auth)
    business_signup_handler = BusinessSignupHandler(business_service, auth)
    test_plan_handler = TestPlanHandler(testplan_service, user_service, auth)
    business_login_handler = BusinessLoginHandler(business_service, auth)
    business_logout_handler = BusinessLogoutHandler(auth)
    create_test_plan_handler = CreateTestPlanHandler(business_service, auth)
    active_test_plan_handler = ActiveTestPlanHandler(testplan_service, user_service, auth)
    profile_user_handler = ProfileHandler(user_service, auth)
    business_test_plan_handler = BusinessTestPlanHandler(business_service, user_service, testplan_service, auth)
    business_profile_handler = BusinessProfileHandler(business_service, auth)

    # Register handlers
    app.add_handler(start_handler.handler)
    app.add_handler(user_signup_handler.handler)
    app.add_handler(user_login_handler.handler)
    app.add_handler(business_signup_handler.handler)
    app.add_handler(business_login_handler.handler)
    app.add_handler(test_plan_handler.handler)
    app.add_handler(create_test_plan_handler.handler)
    app.add_handler(user_logout_handler.handler)
    app.add_handler(business_logout_handler.handler)
    app.add_handler(active_test_plan_handler.handler)
    app.add_handler(business_test_plan_handler.handler)
    # app.add_handler(profile_user_handler.handler)

    # Add multiple handlers from ProfileHandler
    for handler in profile_user_handler.handlers:
        app.add_handler(handler)

    for handler in business_profile_handler.handlers:
        app.add_handler(handler)

    print("Bot is running...")
    app.run_polling()
    db_session.close()

if __name__ == "__main__":
    main()
