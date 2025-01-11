from repositories.TestPlanRepository import TestPlanRepository
from configs.database import SessionLocal


class TestPlanService:
    def __init__(self):
        self.db_session = SessionLocal()
        self.testplan_repo = TestPlanRepository(self.db_session)

    def get_all_testplans(self):
        return self.testplan_repo.get_all_testplans()
    
    def get_testplan_by_id(self, testplan_id: int):
        return self.testplan_repo.get_testplan_by_id(testplan_id)

