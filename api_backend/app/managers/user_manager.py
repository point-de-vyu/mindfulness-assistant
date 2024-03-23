import sqlalchemy
import logging
from api_backend.app.schemes.user import User, UserToCreate
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.db.models.users import User as UserTable
from sqlalchemy.orm import Session


class UserManager:

    def __init__(self, session: Session, logger: logging.Logger) -> None:
        self.db_session = session
        self.logger = logger

    def add_new_user(self, user: UserToCreate, client_id: int) -> int:
        executed_query = self.db_session.execute(
            sqlalchemy.func.add_new_user(
                user.username,
                user.first_name,
                user.last_name,
                client_id,
                user.id_from_client,
            )
        )
        self.db_session.commit()
        user_id = executed_query.scalar()
        if not user_id:
            msg = ErrorMsg.FAILED_DB_RESULT
            self.logger.critical(f"{msg} adding new user")
            raise RuntimeError(msg)
        return user_id

    def get_by_id(self, id: int) -> User | None:
        query = sqlalchemy.select(UserTable).filter_by(id=id)
        executed_query = self.db_session.execute(query)
        user = executed_query.scalar()
        if not user:
            return None
        return user

    def delete_user(self, user_id: int) -> bool:
        executed_query = self.db_session.execute(
            sqlalchemy.func.delete_user_data(user_id)
        )
        self.db_session.commit()
        res = executed_query.scalar()
        if not res:
            self.logger.critical(f"Failed to delete user with {user_id}")
        return res
