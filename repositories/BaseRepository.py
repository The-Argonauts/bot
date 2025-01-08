from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, model):
        self.session.add(model)
        self.session.commit()
        return model

    def get_all(self, model):
        return self.session.query(model).all()

    def get_by_id(self, entity_class, entity_id):
        return self.session.query(entity_class).filter(entity_class.id == entity_id).first()

    def update(self, model):
        self.session.commit()
        return model

    def delete(self, model):
        self.session.delete(model)
        self.session.commit()
        return model