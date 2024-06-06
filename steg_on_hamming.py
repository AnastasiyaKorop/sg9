import collections

import numpy as np
from addit_functs import mod_on_2, reverse_bit
from addit_functs import text_to_binary, subarr_extract, \
    number_to_bin_arr, bin_arr_to_number, binary_to_text

H = np.matrix([
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
], dtype=int)
n = 15


def encode(vector_c, vector_m):
    cod = np.matrix(vector_c, dtype=int)
    m = np.matrix(vector_m, dtype=int)
    s = mod_on_2(H * cod.T)
    s = mod_on_2(s + m.T).T.tolist()[0]

    i = (8 * s[3] + 4 * s[2] + 2 * s[1] + s[0]) - 1
    if i >= 0:
        vector_c = reverse_bit(vector_c, i)

    return vector_c


def decode(vector_c):
    vector_m = mod_on_2(H * np.matrix(vector_c, dtype=int).T)
    vector_m = vector_m.T.tolist()[0]
    return vector_m


def SoH_enc(img, text, start, end, sdvig):
    binary_text = text_to_binary(start) + text_to_binary(text) + text_to_binary(end)
    img_LSB_bit = []

    for byte in img:
        bit_array = number_to_bin_arr(byte)
        img_LSB_bit.append(bit_array[7])

    index = sdvig * n
    for byte in binary_text:
        arr_bit_text = number_to_bin_arr(byte)
        for i in range(0, len(arr_bit_text), 4):
            vector_m = arr_bit_text[i:i + 4]
            vector_c = img_LSB_bit[index:index + n]
            vector_c = encode(vector_c, vector_m)
            img_LSB_bit[index:index + n] = vector_c
            index += n

    new_img = []
    for i in range(len(img_LSB_bit)):
        if i >= len(img):
            break
        bit_array = number_to_bin_arr(img[i])
        bit_array[7] = img_LSB_bit[i]
        byte = bin_arr_to_number(bit_array)
        new_img.append(byte)

    return new_img


def SoH_dec(img, start, end):
    img_LSB_bit = []

    bit_start = []
    for e in text_to_binary(start):
        bit_start = bit_start + number_to_bin_arr(e)

    bit_end = []
    for e in text_to_binary(end):
        bit_end = bit_end + number_to_bin_arr(e)

    for byte in img:
        bit_array = number_to_bin_arr(byte)
        img_LSB_bit.append(bit_array[7])

    text_bit = []
    for i in range(0, len(img_LSB_bit), n):
        vector_c = img_LSB_bit[i:i + n]
        if len(vector_c) < n:
            break
        vector_m = decode(vector_c)
        for bit in vector_m:
            text_bit.append(bit)

    text_bit = subarr_extract(bit_start, text_bit, bit_end)

    text_byte = []
    for i in range(0, len(text_bit), 8):
        byte = bin_arr_to_number(text_bit[i:i + 8])
        text_byte.append(byte)

    return binary_to_text(text_byte)
