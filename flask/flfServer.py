# -*- coding: utf-8 -*-
# @Time    : 2023/7/15 1:44
# @Author  : Kragy
# @File    : flfServer.py

import flask
from flfPicMaker import flfPicMaker
import numpy as np
import cv2
import time

flf = flask.Flask(__name__)


@flf.route('/', methods=['POST'])
def generate_flfPic_by_file():
    if flask.request.content_type.startswith('multipart/form-data'):
        src_bin = flask.request.files.get('file111').read()
    else:
        src_bin = flask.request.data
    img_np_arr = np.frombuffer(src_bin, np.uint8)
    src = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    result = flfPicMaker(src)
    filename = f'log/{time.time()}.png'
    cv2.imwrite(filename, result)
    print(filename)
    return flask.send_file(filename)


if __name__ == '__main__':
    flf.run('0.0.0.0', port=5005)
