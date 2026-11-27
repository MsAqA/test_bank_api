import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session

from src.main.api.fixtures.db_fixture import db_session


@pytest.mark.api

class TestCreateAccount:
    def test_create_account(self, create_user_request, api_manager, db_session: Session):

        response = api_manager.user_steps.create_account(create_user_request)

        assert  response.balance == 0


        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance is not None, "Поле баланса для созданного аккаунта отсутсвует в БД"
        assert account_from_db.id == response.id, "Аккаунт не создан, id аккаунта нет в БД"