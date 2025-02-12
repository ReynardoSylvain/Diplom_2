import allure

@allure.step("Создание нескольких заказов для пользователя")
def create_multiple_orders(api_client, count: int = 1):
    for _ in range(count):
        api_client.place_order(api_client.build_random_burger())