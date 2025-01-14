from configs.database import SessionLocal
from repositories.FeedbackRepository import FeedbackRepository
from repositories.TestPlanRepository import TestPlanRepository


class TestPlanService:
    def __init__(self):
        self.db_session = SessionLocal()
        self.feedback_repo = FeedbackRepository(self.db_session)
        self.testplan_repo = TestPlanRepository(self.db_session)

    def get_all_testplans(self):
        return self.testplan_repo.get_all_testplans()

    def get_feedback(self, testplan_id):
        return self.feedback_repo.get_testplan_feedbacks(testplan_id)
