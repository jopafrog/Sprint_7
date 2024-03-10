import allure
import pytest
import data
from api.api_order import ApiOrder
from api.api_courier import ApiCourier


class TestOrder:
    @allure.title('Проверка создания заказа')
    def test_create_order_success(self):
        response = ApiOrder.create_order(data.payload_order)
        assert response.status_code == 201 and 'track' in response.text

    @allure.title('Проверка создания заказа, с вариантами цветов (Цвет: {color})')
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"]
        ]
    )
    def test_crate_order_diff_colors_success(self, color):
        data.payload_order['color'] = color
        response = ApiOrder.create_order(data.payload_order)

        assert response.status_code == 201 and 'track' in response.text

    @allure.title('Проверка подтверждения заказа')
    def test_accept_order_success(self, create_random_courier):
        courier = create_random_courier
        courier_id = ApiCourier.login_courier(courier[0], courier[1]).json()['id']
        order_track = ApiOrder.create_order(data.payload_order).json()['track']
        order_id = ApiOrder.get_id_order(order_track)

        response = ApiOrder.accept_order(courier_id, order_id)
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @allure.title('Проверка получения списка заказов курьера')
    def test_get_list_orders_success(self, create_random_courier):
        courier = create_random_courier
        courier_id = ApiCourier.login_courier(courier[0], courier[1]).json()['id']
        order_track = ApiOrder.create_order(data.payload_order).json()['track']
        order_id = ApiOrder.get_id_order(order_track)
        ApiOrder.accept_order(courier_id, order_id)

        response = ApiOrder.get_list_orders(courier_id)

        assert (response.status_code == 200 and courier_id == response.json()['orders'][0]['courierId'] and
                order_track == response.json()['orders'][0]['track'])
