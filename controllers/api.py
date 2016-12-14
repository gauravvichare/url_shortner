# -*- coding: utf-8 -*-
import pyqrcode


@request.restful()
def get_qr_code():
    response.view = 'generic.json'
    response.headers['Content-Type'] = 'application/json'
    return dict(GET=_get_qr_code)


def _get_qr_code(**get_params):
    data = get_params['url']
    qr = pyqrcode.create('Unladden swallow')
    return dict(binary_array=qr.code)
