import allure
from src.main.api.foundation.http_requester import HttpRequester
from requests import Response
import requests
from src.main.api.models.base_model import BaseModel
from typing import Optional
from src.main.api.configs.config import Config



class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST {Config.fetch("backendURL")}{self.endpoint.value.url} "):
            allure.attach(str(body), "RequestBody", allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch("backendURL")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )

        allure.attach(response.text, "ResponseBody", allure.attachment_type.JSON)


        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendURL")}{self.endpoint.ADMIN_DELETE_USER.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response