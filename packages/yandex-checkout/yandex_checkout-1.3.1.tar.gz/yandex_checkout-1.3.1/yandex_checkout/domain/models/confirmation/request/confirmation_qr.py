from yandex_checkout.domain.common.confirmation_type import ConfirmationType
from yandex_checkout.domain.models.confirmation.confirmation import Confirmation


class ConfirmationQr(Confirmation):
    """
    Class representing qr confirmation data object
    """

    def __init__(self, *args, **kwargs):
        super(ConfirmationQr, self).__init__(*args, **kwargs)
        if self.type is None or self.type is not ConfirmationType.QR:
            self.type = ConfirmationType.QR
