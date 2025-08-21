import math

from annotated_types.test_cases import cases


class my_math:

    def line_eq(a, b):
        """Находит решение линейного уравнения"""

        # Поиск решения
        roots = -b/a
        return roots

    def quad_eq(a, b, c):
        """Вычисляет корни квадратного уравнения"""
        # Находим дискриминант
        d = b * b - 4 * a * c

        # Поиск корней
        roots = []
        if d > 0:
            roots.append((-b + math.sqrt(d)) / (2 * a))
            roots.append((-b + math.sqrt(d)) / (2 * a))
        elif d == 0:
            roots.append(-b / (2*a))
        else:
            pass
        return roots


print('Поиск решения линейного уравнения')
a = float(input('Введите коэффициент a: '))
b = float(input('Введите коэффициент b: '))

r = my_math.line_eq(a, b)

print(f"Решение линейного уравнения: {r}\n")


print('Расчёт корней квадратного уравнения')
a = float(input('Введите коэффициент a: '))
b = float(input('Введите коэффициент b: '))
c = float(input('Введите коэффициент c: '))

r = my_math.quad_eq(a, b, c)

match len(r):
    case 2:
        print(f"Корни уравнения: {r[0]}, {r[1]}")
    case 1:
        print(f"Корень уравнения: {r[0]}")
    case _:
        print('У уравнения нет действительных корней')