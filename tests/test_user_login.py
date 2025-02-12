import allure
import pytest
from core.api_actions import ApiHandler
from conftest import registered_user_account
from core.data_generator import create_email, create_password
from core.response_messages import LOGIN_FAILED_MESSAGE


@allure.feature('Авторизация пользователей')
class TestAuthSet:
    @allure.title('Успешная авторизация зарегистрированного пользователя')
    @allure.description('Проверка успешной авторизации существующего пользователя')
    def test_user_sign_in_success(self, registered_user_account):
        api_response = registered_user_account.sign_in()
        assert api_response.status_code == 200
        assert api_response.json()['success'] is True

    @allure.title('Неуспешная авторизация с неверным логином')
    @allure.description('Ошибка авторизации при использовании неверного логина')
    @pytest.mark.parametrize('email_address', ['BillyBigger@tarkov.com!', ''])
    def test_user_sign_in_invalid_login_failure(self, registered_user_account, email_address):
        account_creds = registered_user_account.generate_account_data()
        api_response = registered_user_account.sign_in(email_address, account_creds.password)
        assert api_response.status_code == 401
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == LOGIN_FAILED_MESSAGE

    @allure.title('Неуспешная авторизация с неверным паролем')
    @allure.description('Ошибка авторизации при использовании неверного пароля')
    @pytest.mark.parametrize('login_password', ['PassikGym777', ''])
    def test_user_sign_in_invalid_password_failure(self, registered_user_account, login_password):
        account_creds = registered_user_account.generate_account_data()
        api_response = registered_user_account.sign_in(account_creds.email, login_password)
        assert api_response.status_code == 401
        assert api_response.json()['success'] is False
        assert api_response.json()['message'] == LOGIN_FAILED_MESSAGE