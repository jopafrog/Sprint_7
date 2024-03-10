import pytest
import data
from api.api_courier import ApiCourier


@pytest.fixture(scope='function')
def create_random_courier():
    login_pass = ApiCourier.register_new_courier_and_return_login_password()
    yield login_pass

    ApiCourier.delete_courier(ApiCourier.get_courier_id(login_pass[0], login_pass[1]))


@pytest.fixture(scope='function')
def create_static_courier():
    login_pass = data.static_courier
    yield login_pass

    ApiCourier.delete_courier(ApiCourier.get_courier_id(login_pass[0], login_pass[1]))
