import allure
import pytest
import requests
import data
import helpers


class TestOrderCreation:

    @allure.title('Проверка ручки /api/v1/orders. При создании заказа можно:'
                  '1.указать один из цветов — BLACK или GREY;'
                  '2.указать оба цвета;'
                  '3.совсем не указывать цвет;'
                  '4.тело ответа содержит track.')
    @pytest.mark.parametrize('color_variation', data.RANDOM_COLOR)
    def test_order_creation_success(self, color_variation):
        payload = [helpers.create_order_data_without_color(), color_variation]
        order = requests.post(f'{data.URL}{data.CREATE_ORDER_ENDPOINT}', json=payload)
        result = 'track'
        assert order.status_code == 201 and result in order.text, \
            f'status code{order.status_code}, text={order.text}'
