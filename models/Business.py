from __future__ import annotations

from typing import List, Any
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from models.Base import BaseModel
from models.TestPlan import TestPlan
from utilities.PasswordUtils import PasswordUtils


class Business(BaseModel):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)

    test_plans: Mapped[List["TestPlan"]] = relationship()

    def __init__(self, name: str, username: str, password: str, **kw: Any):
        super().__init__(**kw)
        self.name = name
        self.username = username
        self.password = PasswordUtils.hash_password(password)

    def validate_password(self, password: str) -> bool:
        return PasswordUtils.check_password(password, self.password)
