from repositories.TestPlanRepository import TestPlanRepository
from repositories.UserRepository import UserRepository
from repositories.FeedbackRepository import FeedbackRepository
from models.User import User
from models.TestPlan import TestPlan
from configs.database import SessionLocal


class UserService:
    def __init__(self, user_repo: UserRepository, feedback_repo: FeedbackRepository, test_plan_repo: TestPlanRepository):
        self.db_session = SessionLocal()
        self.user_repo = user_repo
        self.feedback_repo = feedback_repo
        self.test_plan_repo = test_plan_repo

    def create_user(self, name: str, username: str, phone_number: str, email: str, password: str):
        user = self.user_repo.get_by_username(username)
        if user:
            raise ValueError("Username already exists.")
        user = User(name=name, username=username,
                    phone_number=phone_number, email=email, password=password)
        self.user_repo.create(user)

    def get_user(self, user_id: int):
        user = self.user_repo.get_by_id(User, user_id)
        if not user:
            raise ValueError("User not found.")
        return user

    def validate_user(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if (not user) or not user.validate_password(password):
            raise ValueError("Username or Password is not valid")
        return user.id

    def sign_up_for_testplan(self, user_id: int, testplan_id: int):
        testplan = self.test_plan_repo.get_by_id(TestPlan, testplan_id)
        user = self.get_user(user_id)
        self.user_repo.add_testplan(user, testplan)

    def get_user_testplans(self, user_id: int):
        user = self.get_user(user_id)
        return user.testplans

    def create_feedback(self, user_id: int, test_plan_id: int, content: str):
        self.feedback_repo.create_user_feedback(user_id, test_plan_id, content)