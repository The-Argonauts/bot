from repositories.BaseRepository import BaseRepository
from models.TestPlan import TestPlan
from datetime import datetime

class TestPlanRepository(BaseRepository):
    def get_by_business(self, business_id):
        return self.session.query(TestPlan).filter(TestPlan.business_id == business_id).all()

    def get_all_testplans(self):
        return self.session.query(TestPlan).filter(datetime.now() < TestPlan.end_date).all()
