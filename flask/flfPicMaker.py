# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 23:58
# @Author  : Kragy
# @File    : flfPicMaker.py

import cv2
import numpy as np

std_shape = (290, 606)  # 标准尺寸
destination = (33, 860)  # 目标位置


def adjustSize(img: np.ndarray):
    """
    调整图片尺寸
    :param img: 要调整的图片
    :return: 调整后的图片
    """
    std_w_h_rate = std_shape[1] / std_shape[0]  # 标准长宽比
    real_w_h_rate = img.shape[1] / img.shape[0]  # 实际长宽比

    # 按比例重设大小
    if real_w_h_rate > std_w_h_rate:
        img = cv2.resize(img, (int(real_w_h_rate * std_shape[0]), std_shape[0]))
    else:
        img = cv2.resize(img, (std_shape[1], int(1 / real_w_h_rate * std_shape[1])))

    # 居中裁剪
    new_img = img[(img.shape[0] - std_shape[0]) // 2:(img.shape[0] - std_shape[0]) // 2 + std_shape[0],
              (img.shape[1] - std_shape[1]) // 2:(img.shape[1] - std_shape[1]) // 2 + std_shape[1]]
    return new_img


def flfPicMaker(src: np.ndarray):
    """
    制作伏拉夫图像
    :param src: 源图像
    :return: 伏拉夫图像
    """
    adjusted_img = adjustSize(src)
    flfTop = cv2.imread('flfTop.png')
    black = np.empty(flfTop.shape).astype(np.uint8)
    black[0:std_shape[0], 0:std_shape[1]] = adjusted_img

    flfTop4 = cv2.imread('flfTop.png', cv2.IMREAD_UNCHANGED)
    mask_d1 = flfTop4[:, :, 3]
    mask_d1 = np.array(mask_d1, dtype=bool)
    mask = np.expand_dims(mask_d1, 2).repeat(3, axis=2)

    matShift = np.float32([[1, 0, destination[0]], [0, 1, destination[1]]])
    dst = cv2.warpAffine(black, matShift, black.shape[0:2][::-1])
    result = flfTop * mask + dst * ~mask
    return result


if __name__ == '__main__':
    src = cv2.imread('src.png')
    cv2.imshow('result', cv2.resize(flfPicMaker(src), (650, 550)))
    cv2.waitKey(0)
    adjustSize(src)
    cv2.imwrite('log/temp.png', flfPicMaker(src))
