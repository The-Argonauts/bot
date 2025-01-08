from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.Base import Base

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    test_plans = relationship('TestPlan', back_populates='business')