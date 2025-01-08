from __future__ import annotations

from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from models.Base import BaseModel
from models.TestPlan import TestPlan


class Business(BaseModel):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    test_plans: Mapped[List["TestPlan"]] = relationship()
