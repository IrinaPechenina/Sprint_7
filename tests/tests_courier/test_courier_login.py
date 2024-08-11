import json

import pytest
import requests
import data
import allure
import helpers


class TestCourierLogin:

    @allure.title('Проверка ручки /api/v1/courier/login. '
                  '1.курьер может авторизоваться;'
                  '2.для авторизации нужно передать все обязательные поля;'
                  '3.успешный запрос возвращает id.')
    def test_courier_login_with_login_password_get_id_success(self):
        courier_login_pass = helpers.generate_courier_return_login_password()  # создан курьер
        response = requests.post(f'{data.URL}{data.COURIER_LOGIN_ENDPOINT}', data=courier_login_pass)  # запрашиваем id
        courier_id = response.json()['id']  # получаем номер id
        result = 'id'
        assert response.status_code == 200 and result in response.text, \
               f'status code{response.status_code}, text={response.text}'
        requests.delete(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}/{courier_id}')

    @allure.title('Проверка ручки /api/v1/courier/login.'
                  '1.курьер не может авторизоваться если неправильно указать логин или пароль;'
                  '2.если авторизоваться под несуществующим пользователем,система вернёт ошибку,')
    def test_courier_login_with_incorrect_login_password_shows_error(self):
        requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', data=helpers.generate_courier_data())
        login_pass_error = data.FAKE_LOGIN_PASSWORD
        response = requests.post(f'{data.URL}{data.COURIER_LOGIN_ENDPOINT}', data=login_pass_error)
        result = data.NOT_FOUND_ERROR
        assert response.status_code == 404 and result in response.text, \
               f'status code{response.status_code}, text={response.text}'

    @allure.title('Проверка ручки /api/v1/courier/login.'
                  '1.курьер не может авторизоваться если какого-то поля нет;'
                  '2.система вернёт ошибку с кодом 400')
    @pytest.mark.parametrize('payload', (data.EMPTY_LOGIN, data.EMPTY_PASSWORD))
    def test_courier_login_without_login_shows_error(self, payload):
        requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', data=helpers.generate_courier_data())
        response = requests.post(f'{data.URL}{data.COURIER_LOGIN_ENDPOINT}', data=payload)
        result = data.BAD_REQUEST_ERROR
        assert response.status_code == 400 and result in response.text, \
               f'status code{response.status_code}, text={response.text}'
