import pytest

from core.api_actions import ApiHandler


@pytest.fixture(scope='function')
def registered_user_account():
    client_instance = ApiHandler()
    client_instance.create_account()
    yield client_instance
    client_instance.remove_account()


@pytest.fixture(scope='function')
def disposable_test_account():
    client_instance: ApiHandler = None
    yield client_instance
    if client_instance:
        client_instance.remove_account()