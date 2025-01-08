from repositories.BaseRepository import BaseRepository
from models.Business import Business

class BusinessRepository(BaseRepository):
    def get_all(self):
        return self.session.query(Business).all()

    def get_by_username(self, username):
        return self.session.query(Business).filter(Business.username == username).first()

    def create_testplan(self, business, testplan):
        # add test plan to the business
        business.test_plans.append(testplan)
        self.session.commit()
