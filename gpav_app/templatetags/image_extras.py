from . import register
from base64 import b64encode


@register.filter
def bin_2_img(_bin):
    if _bin is not None:
        return b64encode(_bin).decode()
