import allure
from dataclasses import dataclass
import requests
import random

from core.data_generator import create_email, create_password, create_username
from core.api_endpoints import BASE_URL, USER_REGISTER_ENDPOINT, USER_DELETE_ENDPOINT, USER_LOGIN_ENDPOINT, USER_LOGOUT_ENDPOINT, USER_CHANGE_ENDPOINT, TOKEN_UPDATE_ENDPOINT, ORDER_CREATE_ENDPOINT, ORDER_USER_ENDPOINT, ORDER_ALL_ENDPOINT, INGREDIENTS_ENDPOINT


@dataclass
class AccountDetails:
    email: str = ''
    password: str = ''
    name: str = ''


class ApiHandler:
    def __init__(self):
        self.account_data: AccountDetails = None
        self.auth_token: str = None
        self.refresh_token_value: str = None

    @staticmethod
    def generate_account_data() -> AccountDetails:
        return AccountDetails(
            email=create_email(),
            password=create_password(),
            name=create_username(),
        )

    def get_email_address(self):
        return self.account_data.email

    def get_login_password(self):
        return self.account_data.password

    def get_display_name(self):
        return self.account_data.name

    def get_account_info(self) -> AccountDetails:
        return self.account_data

    @allure.step('Регистрация нового пользователя: POST /api/auth/register')
    def create_account(self, email: str = '', password: str = '', name: str = ''):
        if not email and not password and not name:
            self.account_data = self.generate_account_data()
        else:
            self.account_data = AccountDetails(email, password, name)
        return requests.post(f"{BASE_URL}{USER_REGISTER_ENDPOINT}", json=self.account_data.__dict__)

    @allure.step('Удаление зарегистрированного пользователя: DELETE /api/auth/user')
    def remove_account(self, auth_token_provided: str = None):
        token_value = auth_token_provided if auth_token_provided else self.auth_token
        return requests.delete(f"{BASE_URL}{USER_DELETE_ENDPOINT}", headers={"Authorization": token_value})

    @allure.step('Авторизация пользователя в системе: POST /api/auth/login')
    def sign_in(self, email: str = '', password: str = ''):
        if not email and not password:
            logging = self.account_data.__dict__
        else:
            logging = {
                "email": email,
                "password": password,
            }

        api_response = requests.post(f"{BASE_URL}{USER_LOGIN_ENDPOINT}", json=logging)
        if api_response.status_code == 200:
            self.auth_token = api_response.json()['accessToken']
            self.refresh_token_value = api_response.json()['refreshToken']

        return api_response

    def sign_out(self):
        return requests.post(f"{BASE_URL}{USER_LOGOUT_ENDPOINT}", json={"token": self.refresh_token_value})

    @allure.step('Изменение данных пользователя: PATCH /api/auth/user')
    def modify_profile(self, email: str = None, password: str = None, name: str = None):
        email_update = email or self.get_email_address()
        password_update = password or self.get_login_password()
        name_update = name or self.get_display_name()

        logging = {
            "email": email_update,
            "password": password_update,
            "name": name_update,
        }

        api_response = requests.patch(f"{BASE_URL}{USER_CHANGE_ENDPOINT}",
                                      headers={"Authorization": self.auth_token}, json=logging)
        if api_response.status_code == 200:
            self.account_data.email = email_update
            self.account_data.password = password_update
            self.account_data.name = name_update

        return api_response

    def renew_token(self):
        logging = {
            "email": self.get_email_address(),
            "password": self.get_login_password(),
        }
        api_response = requests.post(f"{BASE_URL}{TOKEN_UPDATE_ENDPOINT}", json=logging)
        return api_response

    @allure.step('Создание нового заказа: POST /api/orders')
    def place_order(self, order_details: dict):
        return requests.post(f"{BASE_URL}{ORDER_CREATE_ENDPOINT}", json=order_details)

    @allure.step('Получение заказов текущего пользователя: GET /api/orders')
    def fetch_user_orders(self, auth_token_provided: str = None):
        token_value = auth_token_provided if auth_token_provided else self.auth_token
        return requests.get(f"{BASE_URL}{ORDER_USER_ENDPOINT}", headers={"Authorization": token_value})

    @staticmethod
    def retrieve_all_orders():
        return requests.get(f"{BASE_URL}{ORDER_ALL_ENDPOINT}")

    @staticmethod
    def get_ingredient_catalog():
        return requests.get(f"{BASE_URL}{INGREDIENTS_ENDPOINT}")

    @staticmethod
    def build_random_burger() -> dict:
        api_response = ApiHandler().get_ingredient_catalog()
        if not api_response.ok:
            return {}

        data = api_response.json()
        if data.get('success') is not True:
            return {}

        ingredient_hashes = [item['_id'] for item in data["data"]]

        return {"ingredients": random.sample(ingredient_hashes, 3)}