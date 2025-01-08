from repositories.TestPlanRepository import TestPlanRepository
from configs.database import SessionLocal


class UserService:
    def __init__(self):
        self.db_session = SessionLocal()
        self.testplan_repo = TestPlanRepository(self.db_session)

    def get_all_testplans(self):
        return self.testplan_repo.get_all_testplans()

