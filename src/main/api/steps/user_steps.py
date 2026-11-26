from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
             RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
             Endpoint.CREATE_ACCOUNT,
             ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, deposit_request: DepositRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)

        return response

    def deposit_invalid(self, deposit_request: DepositRequest, username: str, password: str):
        response = CrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)

        return response

    def transfer(self, transfer_request: TransferRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def transfer_invalid(self, transfer_request: TransferRequest, username: str, password: str):
        response = CrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_unprocessable()
        ).post(transfer_request)
        return response

    def get_credit(self, get_credit_request: GetCreditRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.GET_CREDIT_ACCOUNT,
            ResponseSpecs.request_created()
        ).post(get_credit_request)
        return response

    def get_credit_invalid(self, get_credit_request: GetCreditRequest, username: str, password: str):
        response = CrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.GET_CREDIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(get_credit_request)
        return response


    def repay_credit(self, repay_credit_request: RepayCreditRequest, username: str, password: str):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.REPAY_CREDIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response


    def repay_credit_invalid(self, repay_credit_request: RepayCreditRequest, username: str, password: str):
        response = CrudRequester(
            RequestSpecs.auth_headers(username, password),
            Endpoint.REPAY_CREDIT_ACCOUNT,
            ResponseSpecs.request_unprocessable()
        ).post(repay_credit_request)
        return response