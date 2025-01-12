from typing import List, Any
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from models.Base import BaseModel
from models.TestPlan import TestPlan
from models.test_plan_users import association_table
from utilities.PasswordUtils import PasswordUtils


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

    def __init__(self, name: str, username: str, phone_number: str, email: str, password: str, **kw: Any):
        super().__init__(**kw)
        self.name = name
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.password = PasswordUtils.hash_password(password)

    def validate_password(self, password: str) -> bool:
        return PasswordUtils.check_password(password, self.password)