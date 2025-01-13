from repositories.BaseRepository import BaseRepository
from models.User import User
from models.test_plan_users import association_table

# repository/user_repository.py


class UserRepository(BaseRepository):
    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def add_testplan(self, user, testplan_id):
        user.testplans.append(testplan_id)
        self.session.commit()
        return user

    def get_users_by_testplan_id(self, testplan_id: int):
        return self.session.query(User).join(association_table, User.id == association_table.c.user_id).filter(association_table.c.test_plan_id == testplan_id).all()
