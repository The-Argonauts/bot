from repositories.BaseRepository import BaseRepository
from models.TestPlan import TestPlan

# repository/test_plan_repository.py
class TestPlanRepository(BaseRepository):
    def get_by_business(self, business_id):
        return self.session.query(TestPlan).filter(TestPlan.business_id == business_id).all()

    def get_all_testplans(self):
        return self.session.query(TestPlan).all()
