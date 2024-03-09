import pytest
from api.api_courier import ApiCourier


class TestCourier:
    def test_registration_courier_success(self, create_static_courier):
        courier = create_static_courier
        response = ApiCourier.registration_courier(courier[0], courier[1], courier[2])

        assert response.status_code == 201 and response.text == '{"ok":true}'

    def test_logining_courier_success(self, create_random_courier):
        courier = create_random_courier
        courier_login = courier[0]
        courier_pass = courier[1]

        response = ApiCourier.login_courier(courier_login, courier_pass)

        assert response.status_code == 200 and 'id' in response.text

    def test_create_courier_and_delete_success(self, create_random_courier):
        courier = create_random_courier
        courier_login = courier[0]
        courier_pass = courier[1]

        response = ApiCourier.delete_courier(ApiCourier.get_courier_id(courier_login, courier_pass))

        assert response.status_code == 200 and response.text == '{"ok":true}'

    def test_create_two_courier_error_create(self, create_random_courier):
        courier = create_random_courier
        courier_login = courier[0]
        courier_pass = courier[1]
        courier_name = courier[2]

        response = ApiCourier.registration_courier(courier_login, courier_pass, courier_name)
        response_text = response.json()['message']

        assert response.status_code == 409 and response_text == 'Этот логин уже используется. Попробуйте другой.'

    @pytest.mark.parametrize(
        "login, password",
        [
            ('', 'test_pass'),
            ('test_login', '')
        ]
    )
    def test_create_courier_bed_parameter_error_create(self, login, password):
        response = ApiCourier.registration_courier(login, password, "Test_name")
        response_text = response.json()['message']

        assert response.status_code == 400 and response_text == 'Недостаточно данных для создания учетной записи'

    def test_logining_courier_bad_password_error_login(self, create_random_courier):
        courier = create_random_courier
        courier_login = courier[0]
        bad_password = '123'

        response = ApiCourier.login_courier(courier_login, bad_password)
        response_text = response.json()['message']

        assert response.status_code == 404 and response_text == 'Учетная запись не найдена'

    def test_logining_courier_bad_login_error_login(self, create_random_courier):
        courier = create_random_courier
        bad_login = 'not_real_courier'
        courier_password = courier[1]

        response = ApiCourier.login_courier(bad_login, courier_password)
        response_text = response.json()['message']

        assert response.status_code == 404 and response_text == 'Учетная запись не найдена'
