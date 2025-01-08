from repositories.BaseRepository import BaseRepository
from models.Business import Business

class BusinessRepository(BaseRepository):
    def get_all(self):
        return self.session.query(Business).all()