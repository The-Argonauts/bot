from __future__ import annotations
from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.Base import BaseModel
from models.Feedback import Feedback

class TestPlan(BaseModel):
    __tablename__ = "test_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    reward = Column(String(100), nullable=False)

    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    feedbacks: Mapped["Feedback"] = relationship()

    def __init__(self, name: str, description: str, start_date: Date, end_date: Date, reward: str, business, **kw: Any):
        super().__init__(**kw)
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.reward = reward
        self.business = business
        self.status = "active"

