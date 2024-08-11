import allure
import requests
import data


class TestOrderList:

    @allure.title('Проверка ручки /api/v1/orders: в тело ответа возвращается список заказов.')
    def test_get_order_list_success(self):
        order_list = requests.get(f'{data.URL}{data.CREATE_ORDER_ENDPOINT}{data.LIMIT_5}')
        result = 'orders'
        assert order_list.status_code == 200 and result in order_list.text, \
            f'status code{order_list.status_code}, text={order_list.text}'
        print(order_list.text)
