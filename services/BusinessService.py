from repositories.BusinessRepository import BusinessRepository
from models.Business import Business
from configs.database import SessionLocal
from models.TestPlan import TestPlan

class BusinessService:
    def __init__(self):
        self.db_session = SessionLocal()
        self.business_repo = BusinessRepository(self.db_session)

    def create_business(self, name: str, username: str, password: str):
        business = self.business_repo.get_by_username(username)
        if business:
            raise ValueError("Username already exists.")
        business = Business(name=name, username=username, password=password)
        self.business_repo.create(business)

    def get_user(self, user_id: int):
        business = self.business_repo.get_by_id(Business, user_id)
        if not business:
            raise ValueError("Business not found.")
        return business

    def create_testplan(self, business: Business, name: str, description: str, start_date: str, end_date: str, reward: str):
        testplan = TestPlan(name=name, description=description, start_date=start_date, end_date=end_date, reward=reward, business=business)
        self.business_repo.create_testplan(business, testplan)

    def validate_business(self, username: str, password: str):
        business = self.business_repo.get_by_username(username)
        if (not business) or business.password != password:
            raise ValueError("Username or Password is not valid")
        return business.id
