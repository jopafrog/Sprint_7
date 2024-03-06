import pytest
from api.api_courier import ApiCourier


class TestCourier:
    def test_add_courier_and_delete_success(self):
        login_pass = ApiCourier.register_new_courier_and_return_login_password()
        courier_login = login_pass[0]
        courier_pass = login_pass[1]

        courier_id = ApiCourier.login_courier(courier_login, courier_pass).json()['id']
        response = ApiCourier.delete_courier(courier_id)

        assert response.status_code == 200 and response.text == '{"ok":true}'

    def test_create_courier_success(self):
        login_pass = ApiCourier.register_new_courier_and_return_login_password()
        courier_login = login_pass[0]
        courier_pass = login_pass[1]

        print(f'log: {courier_login} / pass: {courier_pass}')

        courier_id = ApiCourier.login_courier(courier_login, courier_pass).json()['id']

        assert courier_id != 0

        courier_id = ApiCourier.login_courier(courier_login, courier_pass).json()['id']
        ApiCourier.delete_courier(courier_id)

    def test_create_two_courier_error_create(self):
        login = 'test_courier111222333'
        password = '123'
        first_name = 'Test'

        ApiCourier.create_courier(login, password, first_name)
        response = ApiCourier.create_courier(login, password, first_name)
        response_text = response.json()['message']

        assert response.status_code == 409 and response_text == 'Этот логин уже используется. Попробуйте другой.'

        courier_id = ApiCourier.login_courier(login, password).json()['id']
        ApiCourier.delete_courier(courier_id)

    @pytest.mark.parametrize(
        "login, password",
        [
            ('', 'test_pass'),
            ('test_login', '')
        ]
    )
    def test_create_courier_bed_parameter_error_create(self, login, password):
        response = ApiCourier.create_courier(login, password, "Test_name")
        response_text = response.json()['message']

        assert response.status_code == 400 and response_text == 'Недостаточно данных для создания учетной записи'

