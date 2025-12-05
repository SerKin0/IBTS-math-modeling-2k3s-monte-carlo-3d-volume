import numpy as np
from typing import Callable, Tuple

def monte_carlo_3rd(func: Callable[[np.array, np.array, np.array], bool], 
                    x_lim: Tuple[float, float], 
                    y_lim: Tuple[float, float], 
                    z_lim: Tuple[float, float], 
                    n: int) -> float:    
    """ Вычисление объема функции методом Монте-Карло

    :param func: Функция для расчета объема. Должна принимать списки вещественных значений 
    по трём осям XYZ и возвращать булево значение: находится ли точка внутри области функции.
    :type func: Callable[[np.array, np.array, np.array], bool]
    :param x_lim: Минимальный и максимальный пределы по оси X, в которых будет считаться объем 
    :type x_lim: Tuple[float, float]
    :param y_lim: Минимальный и максимальный пределы по оси Y, в которых будет считаться объем
    :type y_lim: Tuple[float, float]
    :param z_lim: Минимальный и максимальный пределы по оси Z, в которых будет считаться объем
    :type z_lim: Tuple[float, float]
    :param n: Количество точек
    :type n: int
    :return: Объем функции
    :rtype: float
    """
    # Создаем N случайных точек
    x_random = np.random.uniform(*x_lim, n)
    y_random = np.random.uniform(*y_lim, n)
    z_random = np.random.uniform(*z_lim, n)
    
    # Считаем общий объем, в котором находится наша область
    v = (max(x_lim) - min(x_lim)) * (max(y_lim) - min(y_lim)) * (max(z_lim) - min(z_lim))

    # Считаем количество точек, которые находятся внутри функции
    m = np.sum(func(x_random, y_random, z_random))

    # Считаем и возвращаем объем 
    return float(m / n * v)
