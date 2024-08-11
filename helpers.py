import random
import string
import data
from faker import Faker
import requests
import json
import pytest


# метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_courier_data():  # метод возвращает данные курьера логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    # возвращаем тело запроса
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

def generate_courier_data_2():  # метод возвращает данные курьера логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    # возвращаем тело запроса
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

def generate_courier_return_login_password():
    # генерируем логин, пароль и имя курьера
    login_password = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{data.URL}api/v1/courier', json=payload)  # создаем курьера
    # если курьер создан, возвращаем в тест только логин и пароль
    if response.status_code == 201:
        payload_pass = {"login": login, "password": password}
        return payload_pass


def generate_courier_data_without_login():    # метод возвращает список, данные курьера:  пароль, имя
    # генерируем пароль и имя курьера
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "password": password,
        "firstName": first_name
    }


# метод возвращает список, данные курьера:  логин, имя
def generate_courier_data_without_password():
    # генерируем логин и имя курьера
    login = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "login": login,
        "firstName": first_name
    }


def generate_first_name():
    fake = Faker()
    return fake.first_name()


def generate_last_name():
    fake = Faker()
    return fake.last_name()


def generate_street_address():
    fake = Faker()
    return fake.street_address()


def generate_phone_number():
    number = random.randint(111111111,999999999)
    return f'+7{number}'


def generate_number():  # для передачи данных metroStation и rentTime
    number = random.randint(1,10)
    return number


def generate_date():
    fake = Faker()
    return fake.date()


def generate_text():  # для комментария
    fake = Faker()
    return fake.text(10)


def create_order_data_without_color():
    payload_without_color = \
        {
            'firstName': generate_first_name(),
            'lastName': generate_last_name(),
            'address': generate_street_address(),
            'metroStation': generate_number(),
            'phone': generate_phone_number(),
            'rentTime': generate_number(),
            'deliveryDate': generate_date(),
            'comment': generate_text()
        }
    return payload_without_color
