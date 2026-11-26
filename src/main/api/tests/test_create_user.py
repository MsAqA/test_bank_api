import pytest
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from sqlalchemy.orm import Session

@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [
            RandomModelGenerator.generate(CreateUserRequest)
        ]
    )
    def test_create_user_valid(self, api_manager, create_user_request, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert  create_user_request.username == response.username
        assert create_user_request.role == response .role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Созданого пользователя нет в БД"


    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Max15", "Pas!sw0rд"),
            ("Max16", "Pas!sw0"),
            ("Max17", "pas!sw0rd"),
            ("Max18", "PAS!SW0RD"),
            ("Max19", "passw0rd"),
            ("Max20", "pas!sword"),

        ]
    )
    def test_create_user_invalid(self, username, password, api_manager, db_session: Session):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Пользователь создан, ошибка"







