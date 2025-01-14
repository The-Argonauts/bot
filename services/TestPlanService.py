from configs.database import SessionLocal
from models.TestPlan import TestPlan
from repositories.FeedbackRepository import FeedbackRepository
from repositories.TestPlanRepository import TestPlanRepository
from utilities.gemini import Gemini


class TestPlanService:
    def __init__(self, gemini:Gemini=None):
        self.db_session = SessionLocal()
        self.feedback_repo = FeedbackRepository(self.db_session)
        self.testplan_repo = TestPlanRepository(self.db_session)
        self.gemini = gemini

    def get_all_testplans(self):
        return self.testplan_repo.get_all_testplans()

    def get_feedback(self, testplan_id):
        return self.feedback_repo.get_testplan_feedbacks(testplan_id)

    def get_description(self, testplan_id):
        testplan = self.testplan_repo.get_by_id(TestPlan, testplan_id)
        return testplan.description

    def generate_suggestions(self, testplan_description, user_information):
        return self.gemini.suggest_preparation(testplan_description, user_information)
