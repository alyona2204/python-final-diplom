from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

LOGIN = "test1@mail.ru"
PASSWORD = "P@ssw0rd777"

REGISTRATION_URL = reverse('backend:user-register')
USER_DETAIL_URL = reverse('backend:user-details')
USER_LOGIN_URL = reverse('backend:user-login')
USER_REGISTER_CONFIRM_URL = reverse('backend:user-register-confirm')

BASKET_URL = reverse('backend:basket')

PARTNER_UPDATE_URL = reverse('backend:partner-update')
PARTNER_STATE_URL = reverse('backend:partner-state')


class UserTestCase(APITestCase):
    token = ''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()


    def setUp(self):
        print(777)
        # регистрация юзера
        self.registration_endpoint()
        # подтверждение
        self.registration_confirm_endpoint()
        # вход
        self.user_login()
        # так как перевели на celery выключен
        # # загрузка товаров поставщика
        self.partner_update_endpoint()
        # # добавление в корзину
        self.basket_add_endpoint()
        # # выключение магазина и снова добавление в корзину
        self.state_off_basket_add_endpoint()



    def registration_endpoint(self):
        payload = {
            "first_name": "test1",
            "last_name": "test1",
            "email": LOGIN,
            "password": PASSWORD,
            "company": "test1",
            "position": "test1",
            "type": "shop",
        }
        response = self.client.post(REGISTRATION_URL, payload, format='json')

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('Status' in data)
        self.assertTrue(data['Status'])

    def registration_confirm_endpoint(self):
        from backend.models import ConfirmEmailToken
        confirm_token = ConfirmEmailToken.objects.first()
        if not confirm_token:
            self.fail('НЕТ ключей подтверждения')
        payload = {
            "email": "test1@mail.ru",
            "token": confirm_token.key,
        }
        response = self.client.post(USER_REGISTER_CONFIRM_URL, payload, format='json')

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('Status' in data)
        self.assertTrue(data['Status'])

    def user_login(self):
        payload = {
            "email": LOGIN,
            "password": PASSWORD,
        }
        response = self.client.post(USER_LOGIN_URL, payload, format='json')

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('Status' in data)
        self.assertTrue(data['Status'])

        self.assertTrue('Token' in data)

        self.token = data['Token']

    def test_03registration_password_endpoint(self):
        payload = {
            "first_name": "test1",
            "last_name": "test1",
            "email": "test1@mail.ru",
            "password": 'P@ssw0rd',
            "company": "test1",
            "position": "test1"
        }
        response = self.client.post(REGISTRATION_URL, payload, format='json')

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('Status' in data)
        self.assertFalse(data['Status'])

    def test_04user_details_endpoint(self):
        payload = {
        }
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = self.client.get(USER_DETAIL_URL, payload, format='json', headers=headers)

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('id' in data)

    def partner_update_endpoint(self):
        from backend.tasks import get_import
        from backend.models import User
        user = User.objects.last()
        data = get_import(user.id, 'http://0.0.0.0:8000/shop1.yaml')

        self.assertTrue('Status' in data)
        self.assertTrue(data['Status'])

    def basket_add_endpoint(self):
        payload = {
            "items": [
                {
                    "product_info": 1,
                    "quantity": 2
                },
                {
                    "product_info": 2,
                    "quantity": 1
                }
            ]
        }
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = self.client.put(BASKET_URL, payload, format='json', headers=headers)
        print(response.json(), headers)

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('Status' in data)
        self.assertTrue(data['Status'])

    def state_off(self, is403=False):
        payload = {
            "state": "off"
        }
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = self.client.post(PARTNER_STATE_URL, payload, format='json', headers=headers)

        if is403:
            self.assertEqual(response.status_code, 403)
        else:
            self.assertEqual(response.status_code, 200)
            try:
                data = response.json()
            except Exception as e:
                self.fail('Json не читается')

            self.assertTrue('state' in data)
            self.assertEqual(data['state'], 'off')

    def state_on(self, is403=False):
        payload = {
            "state": "on"
        }
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = self.client.post(PARTNER_STATE_URL, payload, format='json', headers=headers)

        if is403:
            self.assertEqual(response.status_code, 403)
        else:
            self.assertEqual(response.status_code, 200)
            try:
                data = response.json()
            except Exception as e:
                self.fail('Json не читается')

            self.assertTrue('state' in data)
            self.assertEqual(data['state'], 'on')

    def state_off_basket_add_endpoint(self):
        self.state_off()
        payload = {
            "items": [
                {
                    "product_info": 1,
                    "quantity": 2
                },
                {
                    "product_info": 2,
                    "quantity": 1
                }
            ]
        }
        headers = {
            'Authorization': f'Token {self.token}'
        }
        response = self.client.put(BASKET_URL, payload, format='json', headers=headers)

        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
        except Exception as e:
            self.fail('Json не читается')

        self.assertTrue('Status' in data)
        self.assertTrue(data['Status'])
        self.state_on()
