from sqlalchemy.orm import Session

from models.user import User


class UserService:

    def __init__(self, db: Session):
        self.db = db

    def get_managers(self):

        managers = (
            self.db.query(User)
            .filter(User.role.has(name="MANAGER"))
            .all()
        )

        return {
            "data": managers
        }