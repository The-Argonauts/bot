from telegram.ext import ApplicationBuilder

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

from handlers.business_handlers.business_test_plan_handler import BusinessTestPlanHandler

from handlers.business_handlers.business_profile_handler import BusinessProfileHandler


def main():
    app = ApplicationBuilder().token(
        "7554909272:AAFj4k-SlOk3aNeDZzP5ucB4dqvonfNM0Gw").build()
    redis_client = RedisClient(host="127.0.0.1", port=6379)
    redis_client.connect()
    auth = Authorization(redis_client)

    start_handler = StartHandler()
    user_signup_handler = UserSignupHandler()
    user_login_handler = UserLoginHandler(auth)
    user_logout_handler = UserLogoutHandler(auth)
    business_signup_handler = BusinessSignupHandler()
    test_plan_handler = TestPlanHandler(auth)
    business_login_handler = BusinessLoginHandler(auth)
    business_logout_handler = BusinessLogoutHandler(auth)
    create_test_plan_handler = CreateTestPlanHandler(auth)
    active_test_plan_handler = ActiveTestPlanHandler(auth)
    profile_user_handler = ProfileHandler(auth)

    business_test_plan_handler = BusinessTestPlanHandler(auth)

    business_profile_handler = BusinessProfileHandler(auth)
    
    cancel_handler = CancelHandler()

    # Register handlers
    app.add_handler(start_handler.handler)
    app.add_handler(user_signup_handler.handler)
    app.add_handler(user_login_handler.handler)
    app.add_handler(business_signup_handler.handler)
    app.add_handler(business_login_handler.handler)
    app.add_handler(cancel_handler.handler)
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


if __name__ == "__main__":
    main()
