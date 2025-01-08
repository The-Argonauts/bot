from sqlalchemy import Column, Integer, String, ForeignKey
from models.Base import Base


class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    rating = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))