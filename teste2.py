import os
from PIL import Image
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import pandas as pd

LIMIAR = 0.007
TAMANHO_DA_IMAGEM = 256
path = "C:\\Users\\Pedro\\PycharmProjects\\iniciacao_cientifica2\\Amostras"


def get_path_image():
    Tk().withdraw()
    filename = askopenfilename()
    return filename


def get_image(path_image):
    image = Image.open(path_image)
    image = image.resize((TAMANHO_DA_IMAGEM, TAMANHO_DA_IMAGEM), Image.ANTIALIAS)
    return image


def image_as_array(image):
    return np.asarray(image)


def fourier_transformer(image):
    image = np.fft.fft(np.fft.fft(image.T).T)
    return np.fft.fftshift(np.fft.fftshift(image))


def calculate_optical_correlation(fft_cal1, fft_cal2):
    img_original_complexa = fft_cal1 / abs(fft_cal1)
    img_2_complexa = fft_cal2 / abs(fft_cal2)
    conjugado_img2 = img_2_complexa.conj()
    result = np.multiply(img_original_complexa, conjugado_img2)
    inverse_fft = np.fft.ifft(result)
    ishift = np.fft.ifftshift(inverse_fft)
    return ishift


def optical_correlation(fft_cal1, fft_cal2):
    ishift = calculate_optical_correlation(fft_cal1, fft_cal2)
    s = np.power(abs(ishift), 2)
    percent_values = test(s)
    if percent_values[0] > percent_values[1] and percent_values[0] > LIMIAR:
        return True
    else:
        return False


def test(matrix):
    quantity_mid = 0
    quantity_matrix = 0
    sum_mid = 0
    sum_matrix = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j == 128:
                quantity_mid += 1
                sum_mid += matrix[i][j]
            else:
                quantity_matrix += 1
                sum_matrix += matrix[i][j]

    percent_mid = sum_mid/quantity_mid
    percent_matrix = sum_matrix/quantity_matrix
    return [percent_mid, percent_matrix]


def main():
    path_image = get_path_image()
    im = get_image(path_image)
    im_array = image_as_array(im)
    fft_cal1 = fourier_transformer(im_array)

    path_image2 = get_path_image()
    im2 = get_image(path_image2)
    im_array2 = image_as_array(im2)
    fft_cal2 = fourier_transformer(im_array2)

    result_optical_correlation = optical_correlation(fft_cal1, fft_cal2)
    print(result_optical_correlation)


main()