from sqlalchemy import Column, Integer, String, ForeignKey
from models.Base import BaseModel

class Feedback(BaseModel):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(2000), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    testplan_id = Column(Integer, ForeignKey('test_plans.id'))