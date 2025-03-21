############################################################################################################
# All right reserved by BGU, 2023
# Author: Arad Gast, Ido Levokovich
# Date: 03/2023
# Description: This code is for calculating the local mean and covariance matrix of a hyperspectral image
#              The code is based on the course of "Hyperspectral Image Processing" by Prof. Stanly Rotman

#############################################################################################################
import numpy as np

PRECISION = np.double


def get_m8(cube, method='local'):
    """This function calculates the 8 neighbors average for subtracting the background,
     including the case when the pixel is on the edge.
    :param cube: the cube of the image
    :param method: the method of calculating the 8 neighbors average or global mean.
    :return: the 8 neighbors average cube in this shape
    """
    row_num, col_num, band_num = cube.shape
    if method == 'local':
        m8cube = np.zeros(shape=(row_num, col_num, band_num), dtype=PRECISION)

        m8cube[1:row_num - 1, 1:col_num - 1] = (cube[1:row_num - 1, 2:col_num] + cube[1:row_num - 1, 0:col_num - 2] +
                                                cube[2:row_num, 1:col_num - 1] + cube[0:row_num - 2, 1:col_num - 1] +
                                                cube[2:row_num, 2:col_num] + cube[2:row_num, 0:col_num - 2] +
                                                cube[0:row_num - 2, 2:col_num] + cube[0:row_num - 2, 0:col_num - 2]) / 8

        # The edge pixels
        m8cube[0, 1:col_num - 1] = np.squeeze(
            (cube[0, 2:col_num] + cube[0, 0:col_num - 2] + cube[1, 1:col_num - 1] + cube[1, 2:col_num] + cube[
                1, 0:col_num - 2]) / 5)
        m8cube[row_num - 1, 1:col_num - 1] = np.squeeze(
            (cube[row_num - 1, 2:col_num] + cube[row_num - 1, 0:col_num - 2] + cube[row_num - 2, 0:col_num - 2] + cube[
                row_num - 2, 1:col_num - 1] + cube[row_num - 2, 2:col_num]) / 5)

        m8cube[1:row_num - 1, 0] = np.squeeze(
            (cube[0:row_num - 2, 0] + cube[2:row_num, 0] + cube[0:row_num - 2, 1] + cube[2:row_num, 1] + cube[
                1:row_num - 1, 1]) / 5)
        m8cube[1:row_num - 1, col_num - 1] = np.squeeze(
            (cube[0:row_num - 2, col_num - 1] + cube[2:row_num, col_num - 1] + cube[0:row_num - 2, col_num - 2] + cube[
                1:row_num - 1, col_num - 2] + cube[2:row_num, col_num - 2]) / 5)

        # The corner pixels
        m8cube[0, 0] = np.squeeze((cube[0, 1] + cube[1, 0] + cube[1, 1]) / 3)
        m8cube[0, col_num - 1] = np.squeeze((cube[0, col_num - 2] + cube[1, col_num - 1] + cube[1, col_num - 2]) / 3)
        m8cube[row_num - 1, 0] = np.squeeze((cube[row_num - 1, 1] + cube[row_num - 2, 0] + cube[row_num - 2, 1]) / 3)
        m8cube[row_num - 1, col_num - 1] = np.squeeze(
            (cube[row_num - 1, col_num - 2] + cube[row_num - 2, col_num - 1] + cube[row_num - 2, col_num - 2]) / 3)

    elif method == 'global':
        m8cube = np.mean(cube, (0, 1))

    else:
        raise ValueError('Method must be "local" or "global"')

    return m8cube


def get_cov8(cube, m8_cube=None, method='local'):
    """This function calculates the covariance matrix of the cube using the 8 neighbors average
    :param cube: the cube of the image
    :param m8_cube: the 8 neighbors average cube
    :param method: the method of calculating the 8 neighbors average or global mean.
    :return: the covariance matrix of the cube
    """
    if m8_cube is None:
        m8_cube = get_m8(cube, method)

    rows, cols, bands = cube.shape
    x = np.subtract(cube, m8_cube, dtype=PRECISION)
    x = x.reshape(rows * cols, bands)  # Flatten to 2D array
    cov = np.cov(x, rowvar=False, bias=True)  # Compute covariance
    return cov


if __name__ == "__main__":
    import spectral as spy

    pass