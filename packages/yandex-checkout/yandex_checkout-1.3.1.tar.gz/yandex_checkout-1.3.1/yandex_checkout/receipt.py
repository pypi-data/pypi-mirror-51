from yandex_checkout.client import ApiClient
from yandex_checkout.domain.common.http_verb import HttpVerb
from yandex_checkout.domain.response.receipt_list_response import ReceiptListResponse


class Receipt:
    base_path = '/receipts'

    def __init__(self):
        self.client = ApiClient()

    @classmethod
    def list(cls, params):
        if ('payment_id' in params or 'refund_id' in params) is False:
            raise TypeError('Invalid params value')

        instance = cls()
        path = cls.base_path

        response = instance.client.request(HttpVerb.GET, path, params)
        return ReceiptListResponse(response)
