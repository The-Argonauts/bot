from repositories.BaseRepository import BaseRepository
from models.Feedback import Feedback

class FeedbackRepository(BaseRepository):
    def get_user_feedbacks(self, user_id):
        return self.session.query(Feedback).filter(Feedback.user_id == user_id).all()

    def get_testplan_feedbacks(self, testplan_id):
        return self.session.query(Feedback).filter(Feedback.testplan_id == testplan_id).all()

    def create_user_feedback(self, user_id, testplan_id, content):
        feedback = Feedback(user_id=user_id, testplan_id=testplan_id,content=content)
        self.session.add(feedback)
        self.session.commit()