import pytest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session


class TestTransfer:

        @pytest.mark.parametrize(
            "create_user_request",
            [
                RandomModelGenerator.generate(CreateUserRequest)
            ]
        )
        def test_transfer(self, api_manager, create_user_request, db_session: Session):
            response = api_manager.admin_steps.create_user(create_user_request)

            assert create_user_request.username == response.username
            assert create_user_request.role == response.role

            response = api_manager.user_steps.create_account(create_user_request)

            assert response.balance == 0
            account_id1 = response.id

            response = api_manager.user_steps.create_account(create_user_request)

            assert response.balance == 0
            account_id2 = response.id

            deposit_request = DepositRequest(accountId=account_id1, amount=5000)
            response = api_manager.user_steps.deposit(deposit_request, create_user_request.username, create_user_request.password)

            assert response.balance == 5000


            transfer_request = TransferRequest(fromAccountId=account_id1, toAccountId=account_id2, amount=4500)
            response = api_manager.user_steps.transfer(transfer_request, create_user_request.username, create_user_request.password)

            assert response.fromAccountIdBalance == 500

            db_session.expire_all()

            account_from_db1 = Account.get_account_by_id(db_session, account_id1)
            account_from_db2 = Account.get_account_by_id(db_session, account_id2)

            assert account_from_db1 is not None, "Счёт отправителя отсутствует в БД"
            assert account_from_db2 is not None, "Счёт получателя отсутствует в БД"

            assert account_from_db1.balance == 500
            assert account_from_db2.balance == 4500

        @pytest.mark.parametrize(
            "create_user_request",
            [
                RandomModelGenerator.generate(CreateUserRequest)
            ]
        )
        def test_transfer_invalid(self, api_manager, create_user_request, db_session: Session):
            response = api_manager.admin_steps.create_user(create_user_request)

            assert create_user_request.username == response.username
            assert create_user_request.role == response.role

            response = api_manager.user_steps.create_account(create_user_request)

            assert response.balance == 0
            account_id1 = response.id

            response = api_manager.user_steps.create_account(create_user_request)

            assert response.balance == 0
            account_id2 = response.id

            deposit_request = DepositRequest(accountId=account_id1, amount=5000)
            response = api_manager.user_steps.deposit(deposit_request, create_user_request.username, create_user_request.password)

            assert response.balance == 5000

            transfer_request = TransferRequest(fromAccountId=account_id1, toAccountId=account_id2, amount=5500)
            response = api_manager.user_steps.transfer_invalid(transfer_request, create_user_request.username, create_user_request.password)

            assert response.json()["error"] == "Insufficient funds. Current balance: 5000.00, required: 5500.00"

            db_session.expire_all()

            account_from_db1 = Account.get_account_by_id(db_session, account_id1)
            account_from_db2 = Account.get_account_by_id(db_session, account_id2)

            assert account_from_db1 is not None, "Счёт отправителя отсутствует в БД"
            assert account_from_db2 is not None, "Счёт получателя отсутствует в БД"

            assert account_from_db1.balance == 5000
            assert account_from_db2.balance == 0
