import allure
import pytest
from core.api_actions import ApiHandler
from conftest import disposable_test_account
from core.data_generator import create_email, create_password, create_username
from core.response_messages import EXISTING_USER_ACCOUNT_MESSAGE, REQUIRED_USER_DATA_MISSING_MESSAGE


@allure.feature('Регистрация пользователей')
class TestRegistrationSet:
    @allure.title('Успешная регистрация уникального пользователя')
    @allure.description('Проверка успешной регистрации нового уникального пользователя')
    def test_account_creation_unique_user_success(self, disposable_test_account):
        disposable_test_account = ApiHandler()
        api_response = disposable_test_account.create_account()
        assert api_response.status_code == 200
        assert api_response.json()['success'] is True

    @allure.title('Регистрация уже существующего пользователя')
    @allure.description('Ошибка при попытке повторной регистрации существующего пользователя')
    def test_account_creation_existing_user_failure(self):
        api_client = ApiHandler()
        api_client.create_account()
        api_response = api_client.create_account(
            api_client.get_email_address(), 'UserokPassik777', api_client.get_display_name())
        assert api_response.status_code == 403
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == EXISTING_USER_ACCOUNT_MESSAGE

    @allure.title('Регистрация пользователя с пропуском обязательного поля')
    @allure.description('Ошибка при регистрации пользователя, если не заполнено одно из обязательных полей (email, password, name)')
    @pytest.mark.parametrize('data_field', ['email', 'password', 'name'])
    def test_account_creation_missing_field_failure(self, data_field):
        api_client = ApiHandler()
        account_creds = api_client.generate_account_data()
        setattr(account_creds, data_field, '')
        api_response = api_client.create_account(account_creds.email, account_creds.password, account_creds.name)
        assert api_response.status_code == 403
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == REQUIRED_USER_DATA_MISSING_MESSAGE