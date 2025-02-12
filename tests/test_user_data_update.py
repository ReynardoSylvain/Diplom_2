import allure
import pytest

from core.api_actions import ApiHandler
from conftest import registered_user_account
from core.data_generator import create_email, create_password, create_username
from core.response_messages import AUTH_REQUIRED_MESSAGE, USER_EMAIL_CONFLICT_MESSAGE


@allure.feature('Изменение данных пользователя')
class TestProfileUpdateSet:
    @allure.title('Успешное изменение данных пользователя')
    @allure.description('Проверка возможности изменения email, пароля или имени пользователя')
    @pytest.mark.parametrize('email_update, password_update, name_update', [
        (create_email(), None, None),
        (None, create_password(), None),
        (None, None, create_username()),
    ])
    def test_profile_modification_success(self, registered_user_account, email_update, password_update, name_update):
        registered_user_account.sign_in()
        api_response = registered_user_account.modify_profile(email=email_update, password=password_update, name=name_update)
        assert api_response.status_code == 200
        assert api_response.json()['success'] is True

    @allure.title('Неуспешное изменение данных пользователя без авторизации')
    @allure.description('Ошибка при попытке изменения данных пользователя, если пользователь не авторизован')
    @pytest.mark.parametrize('email_update, password_update, name_update', [
        (create_email(), None, None),
        (None, create_password(), None),
        (None, None, create_username()),
    ])
    def test_profile_modification_unauthorized_failure(self, registered_user_account, email_update, password_update, name_update):
        api_response = registered_user_account.modify_profile(email=email_update, password=password_update, name=name_update)
        assert api_response.status_code == 401
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == AUTH_REQUIRED_MESSAGE

    @allure.title('Неуспешное изменение email на уже зарегистрированный')
    @allure.description('Ошибка при попытке изменить email на тот, который уже используется другим пользователем')
    def test_profile_modification_email_conflict_failure(self, registered_user_account):
        another_user = ApiHandler()
        another_user.create_account()
        registered_user_account.sign_in()
        api_response = registered_user_account.modify_profile(email=another_user.get_email_address())
        assert api_response.status_code == 403
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == USER_EMAIL_CONFLICT_MESSAGE