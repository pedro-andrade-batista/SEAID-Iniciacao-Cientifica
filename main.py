import os
from PIL import Image
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import Tk


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


def optical_correlation(fft_cal1, fft_cal2):
    ishift = calculate_optical_correlation(fft_cal1, fft_cal2)
    s = np.power(abs(ishift), 2)
    percent_values = test(s)
    if percent_values[0] > percent_values[1] and percent_values[0] > LIMIAR:
        return True
    else:
        return False


def calculate_optical_correlation(fft_cal1, fft_cal2):
    img_original_complexa = fft_cal1 / abs(fft_cal1)
    img_2_complexa = fft_cal2 / abs(fft_cal2)
    conjugado_img2 = img_2_complexa.conj()
    result = np.multiply(img_original_complexa, conjugado_img2)
    inverse_fft = np.fft.ifft(result)
    ishift = np.fft.ifftshift(inverse_fft)
    return ishift


def walk_directories_falsos_negativos(directory):
    falso_negativo = 0
    for root, dirs, files in os.walk(directory[0]):
        try:
            image_base = get_image(root + "\\" + files[0])
            image_base_array = image_as_array(image_base)
            fft_cal1 = fourier_transformer(image_base_array)
        except IndexError:
            continue
        for sample in files:
            try:
                im2 = get_image(root + "\\" + sample)
                img2_array = image_as_array(im2)
                fft_cal2 = fourier_transformer(img2_array)
                same = optical_correlation(fft_cal1, fft_cal2)
                if not same:
                    falso_negativo += 1
            except OSError:
                print("não foi possivel converter a imagem")
    return falso_negativo


def walk_directories_falsos_positivos(directory):
    falsos_positivos = 0
    path_image = get_path_image()
    im = get_image(path_image)
    im_array = image_as_array(im)
    fft_cal1 = fourier_transformer(im_array)
    for root, dirs, files in os.walk(directory[0]):
        for sample in files:
            try:
                im2 = get_image(root + "\\" + sample)
                img2_array = image_as_array(im2)
                fft_cal2 = fourier_transformer(img2_array)
                same = optical_correlation(fft_cal1, fft_cal2)
                if same:
                    falsos_positivos += 1
                break
            except OSError:
                print("não foi possivel converter a imagem")
    return falsos_positivos


def test(matrix):
    quantity_mid = 0
    quantity_matrix = 0
    sum_mid = 0
    sum_matrix = 0
    for i in range(len(matrix)): # i == linhas
        for j in range(len(matrix)): # j == colunas
            if j == 128:
                quantity_mid += 1
                sum_mid += matrix[i][j]
            else:
                quantity_matrix += 1
                sum_matrix += matrix[i][j]

    percent_mid = sum_mid / quantity_mid
    percent_matrix = sum_matrix / quantity_matrix
    return [percent_mid, percent_matrix]


def main():
    cont = 0
    directory = [x[0] for x in os.walk(path)]

    falso_negativo = walk_directories_falsos_negativos(directory)
    falso_positivo = walk_directories_falsos_positivos(directory)

    print(f'Falso Negativo: {falso_negativo}')
    print(f'Falso Positivo: {falso_positivo}')


main()
