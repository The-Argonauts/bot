from repositories.BaseRepository import BaseRepository
from models.User import User

# repository/user_repository.py
class UserRepository(BaseRepository):
    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def add_testplan(self, user, testplan):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", user.id, testplan.id)
        user = self.session.query(User).get(user.id)
        testplan = self.session.query(testplan).get(id)
        user.testplans.append(testplan)
        self.session.commit()
        return user