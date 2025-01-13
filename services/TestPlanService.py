from repositories.TestPlanRepository import TestPlanRepository
from configs.database import SessionLocal
from repositories.FeedbackRepository import FeedbackRepository


class TestPlanService:
    def __init__(self):
        self.db_session = SessionLocal()
        self.testplan_repo = TestPlanRepository(self.db_session)
        self.feedback_repo = FeedbackRepository(self.db_session)

    def get_all_testplans(self):
        return self.testplan_repo.get_all_testplans()

    def get_feedback(self, id):
        return self.feedback_repo.get_testplan_feedbacks(id)

    def get_users(self, testplan_id: int):
        return self.user_repo.get_users_by_testplan_id(testplan_id)
