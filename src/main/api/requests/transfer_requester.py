from src.main.api.requests.requester import Requester
import requests
from requests import Response
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from http import HTTPStatus



class TransferRequester(Requester):
    def post(self, transfer_request: TransferRequest) -> TransferResponse | Response:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_request.model_dump(),
            headers=self.headers,
        )

        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK]:
            return TransferResponse(**response.json())

        return response