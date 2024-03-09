import requests


class ApiOrder:
    @staticmethod
    def create_order(order: dict):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=order)

        return response

    @staticmethod
    def accept_order(courier_id, order_id):
        payload = {
            "courierId": int(courier_id)
        }
        response = requests.put(
            f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{order_id}', params=payload)

        return response

    @staticmethod
    def get_id_order(track_order):
        payload = {
            "t": track_order
        }
        response = requests.get(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/track', params=payload)

        return response.json()['order']['id']

    @staticmethod
    def get_list_orders(courier_id):
        payload = {
            "courierId": int(courier_id)
        }
        response = requests.get(f'https://qa-scooter.praktikum-services.ru/api/v1/orders', params=payload)

        return response
