import pytest
from src.main.api.models.login_user_request import LoginUserRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.fixtures.db_fixture import db_session


@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self, api_manager, db_session: Session):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        user_from_db = User.get_user_by_username(db_session, login_user_request.username)
        assert user_from_db is not None, "Admin отсутствует в БД"

        response =  api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

        assert user_from_db.username == response.user.username
        assert user_from_db.role == response.user.role

    def test_login_user(self, api_manager, create_user_request, db_session: Session):

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is not None, "User отсутствует в БД"


        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username
        assert  response.user.role == "ROLE_USER"

        assert user_from_db.username == response.user.username
        assert user_from_db.role == response.user.role








