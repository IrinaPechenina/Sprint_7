import pytest
import requests
import data
import allure
import helpers


class TestCourierCreation:

    @allure.title('Проверка ручки /api/v1/courier. '
                  '1.курьера можно создать'
                  '2.чтобы создать курьера, нужно передать в ручку все обязательные поля'
                  '3.успешный запрос возвращает {"ok":true}'
                  '4.запрос возвращает код ответа 201.')
    def test_create_courier_with_unique_login_success(self):
        courier_data = helpers.generate_courier_data()
        response = requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', json=courier_data)
        result = data.RESPONSE_OK
        assert response.status_code == 201 and result == response.text, \
            f'status code{response.status_code}, text={response.text}'
        courier_login = requests.post(f'{data.URL}{data.COURIER_LOGIN_ENDPOINT}', json=courier_data)
        requests.delete(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}{courier_login.json()['id']}')
        print(response.text, response.status_code)

    @allure.title('Проверка ручки /api/v1/courier. '
                  '1.нельзя создать двух одинаковых курьеров;'
                  '2.если создать пользователя с логином, который уже есть, то возвращается ошибка.'
                  '3.запрос возвращает код ответа 409 и содержит текст "Этот логин уже используется".')
    def test_create_courier_with_existing_login_shows_error_409(self):
        courier_data = helpers.generate_courier_data()
        response = requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', json=courier_data)
        response2 = requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', json=courier_data)
        result = data.ERROR_EXISTING_LOGIN
        assert response2.status_code == 409 and result in response2.text, \
            (
                f'status code{response.status_code}, text={response.text}'
            )
        courier_login = requests.post(f'{data.URL}{data.COURIER_LOGIN_ENDPOINT}', json=courier_data)
        requests.delete(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}{courier_login.json()['id']}')

    @allure.title('Проверка ручки /api/v1/courier. '
                  '1.нельзя создать курьера без параметра "логин"'
                  '2.запрос возвращает ошибку "Недостаточно данных для создания учетной записи"'
                  '3.запрос возвращает код ответа 400.')
    def test_create_courier_without_login_shows_error_400(self):
        courier_data = helpers.generate_courier_data_without_login()
        response = requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', json=courier_data)
        result = data.ERROR_INCOMPLETE_DATA
        assert response.status_code == 400 and result in response.text, \
            f'status code{response.status_code}, text={response.text}'

    @allure.title('Проверка ручки /api/v1/courier. '
                  '1.нельзя создать курьера без параметра "пароль"'
                  '2.запрос возвращает ошибку "Недостаточно данных для создания учетной записи"'
                  '3.запрос возвращает код ответа 400.')
    def test_create_courier_without_password_shows_error_400(self):
        courier_data = helpers.generate_courier_data_without_password()
        response = requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', json=courier_data)
        result = data.ERROR_INCOMPLETE_DATA
        assert response.status_code == 400 and result in response.text, \
            f'status code{response.status_code}, text={response.text}'

    @allure.title('Проверка ручки /api/v1/courier. '
                  '1.нельзя создать курьера без заполненного поля пароля или логина'
                  '2.запрос возвращает ошибку "Недостаточно данных для создания учетной записи"'
                  '3.запрос возвращает код ответа 400.')
    @pytest.mark.parametrize('courier_data', (data.WITHOUT_PASSWORD, data.WITHOUT_LOGIN))
    def test_create_courier_empty_login_or_password_shows_error_400(self, courier_data):
        response = requests.post(f'{data.URL}{data.CREATE_COURIER_ENDPOINT}', json=courier_data)
        result = data.ERROR_INCOMPLETE_DATA
        assert response.status_code == 400 and result in response.text, \
            f'status code{response.status_code}, text={response.text}'
        print(response.status_code, response.text)

