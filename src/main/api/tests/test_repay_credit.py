import pytest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models. create_credit_user_request import CreateCreditUserRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session



class TestRepayCredit:
    @pytest.mark.parametrize(
        "create_user_request",
        [
            RandomModelGenerator.generate(CreateCreditUserRequest)
        ]
    )
    def test_repay_credit(self, api_manager, create_user_request, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        account_id = response.id

        get_credit_request = GetCreditRequest(accountId=account_id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.get_credit(get_credit_request, create_user_request.username, create_user_request.password)

        credit_id = credit_response.creditId

        repay_credit_request = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=5000)
        response = api_manager.user_steps.repay_credit(repay_credit_request, create_user_request.username, create_user_request.password)

        assert response.creditId == credit_id
        assert response.amountDeposited == 5000

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, account_id)

        assert account_from_db is not None, "Account отсутствует в БД"
        assert account_from_db.balance == 0

    @pytest.mark.parametrize(
        "create_user_request",
        [
            RandomModelGenerator.generate(CreateCreditUserRequest)
        ]
    )
    def test_repay_credit_invalid(self, api_manager, create_user_request, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        account_id = response.id

        get_credit_request = GetCreditRequest(accountId=account_id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.get_credit(get_credit_request, create_user_request.username, create_user_request.password)

        credit_id = credit_response.creditId

        repay_credit_request = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=4000)
        response = api_manager.user_steps.repay_credit_invalid(repay_credit_request, create_user_request.username, create_user_request.password)


        assert response.json()["error"] == "The amount is not enough. Credit balance: -5000"

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, account_id)

        assert account_from_db is not None, "Account отсутствует в БД"
        assert account_from_db.balance == 5000



