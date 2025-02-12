import allure
import pytest

from core.api_actions import ApiHandler
from core.response_messages import INGREDIENT_HASH_MISSING_MESSAGE, AUTH_REQUIRED_MESSAGE
from conftest import registered_user_account


@allure.feature('Создание заказов')
class TestOrderSet:
    @allure.title('Заказ с авторизацией пользователя')
    @allure.description('Успешное создание заказа при наличии авторизации')
    def test_order_placement_authorized_user_success(self, registered_user_account):
        registered_user_account.sign_in()
        order_list = registered_user_account.build_random_burger()
        api_response = registered_user_account.place_order(order_list)
        assert api_response.status_code == 200
        assert api_response.json()['success'] is True


    @allure.title('Заказ без авторизации пользователя')
    @allure.description('Ошибка при создании заказа без авторизации')
    def test_order_placement_unauthorized_user_failure(self, registered_user_account):
        api_response = registered_user_account.place_order(ApiHandler().build_random_burger())
        assert api_response.status_code == 400
        assert api_response.json()["success"] is False
        # этот тест постоянно выбивает ошибку и код ответа 200


    @allure.title('Заказ без ингредиентов')
    @allure.description('Ошибка при создании заказа, если не указаны ингредиенты')
    def test_order_placement_no_ingredients_failure(self, registered_user_account):
        registered_user_account.sign_in()
        api_response = registered_user_account.place_order({"ingredients": []})
        assert api_response.status_code == 400
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == INGREDIENT_HASH_MISSING_MESSAGE

    @allure.title('Заказ с некорректным хешем ингредиентов')
    @allure.description('Ошибка при создании заказа с невалидными идентификаторами ингредиентов')
    @pytest.mark.parametrize('bad_hash', ['ay1yayay12y42yaayre4', 'yayayayyaayay', 'billy', '8'])
    def test_order_placement_invalid_hash_failure(self, registered_user_account, bad_hash):
        bad_hash_order = {"ingredients": bad_hash}
        registered_user_account.sign_in()
        api_response = registered_user_account.place_order(bad_hash_order)
        assert api_response.status_code == 500

        response_text = api_response.text
        assert "Internal Server Error" in response_text, "Response text should contain 'Internal Server Error' for 500 error"