from sqlalchemy import Table, Column, Integer, ForeignKey
from models.Base import BaseModel

association_table = Table(
    'test_plan_users',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('test_plan_id', Integer, ForeignKey('test_plans.id'), primary_key=True)
)
