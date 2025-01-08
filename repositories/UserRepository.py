from repositories.BaseRepository import BaseRepository
from models.User import User

# repository/user_repository.py
class UserRepository(BaseRepository):
    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
