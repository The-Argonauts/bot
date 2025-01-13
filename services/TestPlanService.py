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

    def get_feedback(self, testplan_id):
        return self.testplan_repo.get_testplan_feedbacks(testplan_id)
    
    def get_by_id(self, testplan_id):
        return self.testplan_repo.get_by_id(testplan_id)
