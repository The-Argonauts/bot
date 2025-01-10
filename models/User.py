from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from models.Base import BaseModel
from models.TestPlan import TestPlan
from models.TestPlanUser import association_table


class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    testplans: Mapped[List[TestPlan]] = relationship(secondary=association_table)
    feedbacks: Mapped[List["Feedback"]] = relationship()