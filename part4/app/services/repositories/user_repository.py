from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_all_user(self):
        return self.model.query.all()

    def put_user(self, user_id, new_data):
        user = self.get(user_id)
        if user:
            for key, value in new_data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None
        
    def get_user(self, user_id):
        return self.get(user_id)

    def create_user(self, user_data):
        new_user = User(**user_data)
        self.add(new_user)
        return new_user
