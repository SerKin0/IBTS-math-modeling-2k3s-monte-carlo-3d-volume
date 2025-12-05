from monte_carlo import monte_carlo_3rd

def check_inside_function(x: float, y: float, z: float) -> bool:
    """Проверяем, находится ли введенная точка внутри функции

    :param x: Координата по оси X
    :type x: float
    :param y: Координата по оси Y
    :type y: float
    :param z: Координата по оси Z
    :type z: float
    :return: Если находится внутри, то True, иначе False
    :rtype: bool
    """
    return (x*x + y*y - 1 <= z*z) & (z*z <= 3/5 * (x*x + y*y + 1))


V = monte_carlo_3rd(
    func=check_inside_function,
    x_lim=(-3, 3),
    y_lim=(-3, 3),
    z_lim=(-3, 3),
    n=1_000_000
)

print(f"{V=}")