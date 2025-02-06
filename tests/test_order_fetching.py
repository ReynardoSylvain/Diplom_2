import allure
import pytest

from core.api_actions import ApiHandler
from core.response_messages import AUTH_REQUIRED_MESSAGE
from conftest import registered_user_account


@allure.feature('Получение информации о заказах')
class TestOrderRetrievalSet:
    @allure.title('Получение заказов авторизованным пользователем')
    @allure.description('Успешное получение списка заказов для авторизованного пользователя')
    def test_fetch_orders_authorized_user_success(self, registered_user_account):
        registered_user_account.sign_in()
        for _ in range(2):
            registered_user_account.place_order(ApiHandler().build_random_burger())

        api_response = registered_user_account.fetch_user_orders()
        assert api_response.status_code == 200
        assert api_response.json()["success"] is True

    @allure.title('Получение заказов неавторизованным пользователем')
    @allure.description('Ошибка при попытке получения заказов без авторизации')
    def test_fetch_orders_unauthorized_user_failure(self, registered_user_account):
        api_response = registered_user_account.fetch_user_orders()
        assert api_response.status_code == 401
        assert api_response.json()["success"] is False
        assert api_response.json()["message"] == AUTH_REQUIRED_MESSAGE