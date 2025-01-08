from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.Base import BaseModel


class TestPlan(BaseModel):
    __tablename__ = "test_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    reward = Column(String, nullable=False)

    business_id = Column(Integer, ForeignKey("businesses.id"))
    business = relationship("Business", back_populates="test_plans")

    def __init__(self, name: str, description: str, start_date: str, end_date: str, reward: str, business):
        super().__init__()
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.reward = reward
        self.business = business
        self.status = "active"

