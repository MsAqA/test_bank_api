import pytest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session
from sqlalchemy.orm import Session




class TestDeposit:

    @pytest.mark.parametrize(
        "create_user_request",
        [
            RandomModelGenerator.generate(CreateUserRequest)
        ]
    )
    def test_deposit(self, api_manager, create_user_request, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        account_id = response.id

        deposit_request = DepositRequest(accountId=account_id, amount=5000)
        response = api_manager.user_steps.deposit(deposit_request, create_user_request.username, create_user_request.password)

        assert response.balance == 5000

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, account_id)

        assert account_from_db is not None, "Account отсутствует в БД"
        assert account_from_db.balance == 5000
        assert account_from_db.balance == response.balance

    @pytest.mark.parametrize(
        "create_user_request",
        [
            RandomModelGenerator.generate(CreateUserRequest)
        ]
    )
    def test_deposit_invalid(self, api_manager, create_user_request, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        account_id = response.id

        deposit_request = DepositRequest(accountId=account_id, amount=500)
        response = api_manager.user_steps.deposit_invalid(deposit_request, create_user_request.username, create_user_request.password)



        assert response.json()["error"] == "Amount must be between 1000 and 9000"

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, account_id)

        assert account_from_db is not None
        assert account_from_db.balance == 0




