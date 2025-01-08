from telegram.ext import ApplicationBuilder

from handlers.business_handlers.signup_handler import BusinessSignupHandler
from handlers.start_handler import StartHandler
from handlers.user_handlers.login_handler import UserLoginHandler
from handlers.user_handlers.signup_handler import UserSignupHandler
from handlers.cancel_handler import CancelHandler


def main():
    app = ApplicationBuilder().token("7554909272:AAFj4k-SlOk3aNeDZzP5ucB4dqvonfNM0Gw").build()

    start_handler = StartHandler()
    user_signup_handler = UserSignupHandler()
    user_login_handler = UserLoginHandler()
    business_signup_handler = BusinessSignupHandler()
    cancel_handler = CancelHandler()

    # Register handlers
    app.add_handler(start_handler.handler)
    app.add_handler(user_signup_handler.handler)
    app.add_handler(user_login_handler.handler)
    app.add_handler(business_signup_handler.handler)
    app.add_handler(cancel_handler.handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
