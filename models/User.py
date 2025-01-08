from sqlalchemy import  Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.Base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    test_plans = relationship("TestPlan", back_populates="business")