import math
import unittest

from annotated_types.test_cases import cases


class my_math:

    def line_eq(a, b):
        """Находит решение линейного уравнения"""

        # Поиск решения
        if a != 0:
            roots = -b/a
        else:
            roots = None
        return roots

    def quad_eq(a, b, c):
        """Вычисляет корни квадратного уравнения"""
        # Находим дискриминант
        d = b * b - 4 * a * c

        # Поиск корней
        roots = []
        if d > 0:
            roots.append((-b + math.sqrt(d)) / (2 * a))
            roots.append((-b - math.sqrt(d)) / (2 * a))  # Fixed: was using + instead of -
        elif d == 0:
            roots.append(-b / (2*a))
        else:
            pass
        return roots


class TestMyMath(unittest.TestCase):
    """Unit tests for my_math class methods"""
    
    def test_line_eq_basic(self):
        """Test basic linear equation solving"""
        # Test: 2x + 3 = 0 -> x = -1.5
        result = my_math.line_eq(2, 3)
        self.assertEqual(result, -1.5)
        
        # Test: 5x - 10 = 0 -> x = 2
        result = my_math.line_eq(5, -10)
        self.assertEqual(result, 2)
        
        # Test: -3x + 6 = 0 -> x = 2
        result = my_math.line_eq(-3, 6)
        self.assertEqual(result, 2)
    
    def test_line_eq_zero_coefficients(self):
        """Test linear equation with zero coefficients"""
        # Test: 0x + 5 = 0 -> should return None
        result = my_math.line_eq(0, 5)
        self.assertEqual(result, None)
        
        # Test: 2x + 0 = 0 -> x = 0
        result = my_math.line_eq(2, 0)
        self.assertEqual(result, 0)
    
    def test_quad_eq_two_roots(self):
        """Test quadratic equation with two real roots"""
        # Test: x² - 5x + 6 = 0 -> x = 2, x = 3
        result = my_math.quad_eq(1, -5, 6)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0], 3.0, places=10)
        self.assertAlmostEqual(result[1], 2.0, places=10)
        
        # Test: x² + x - 6 = 0 -> x = 2, x = -3
        result = my_math.quad_eq(1, 1, -6)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0], 2.0, places=10)
        self.assertAlmostEqual(result[1], -3.0, places=10)
    
    def test_quad_eq_one_root(self):
        """Test quadratic equation with one real root (discriminant = 0)"""
        # Test: x² - 4x + 4 = 0 -> x = 2 (double root)
        result = my_math.quad_eq(1, -4, 4)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], 2.0, places=10)
        
        # Test: x² + 2x + 1 = 0 -> x = -1 (double root)
        result = my_math.quad_eq(1, 2, 1)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], -1.0, places=10)
    
    def test_quad_eq_no_real_roots(self):
        """Test quadratic equation with no real roots (discriminant < 0)"""
        # Test: x² + 1 = 0 -> no real roots
        result = my_math.quad_eq(1, 0, 1)
        self.assertEqual(len(result), 0)
        
        # Test: x² + 2x + 5 = 0 -> no real roots
        result = my_math.quad_eq(1, 2, 5)
        self.assertEqual(len(result), 0)
    
    def test_quad_eq_zero_coefficient_a(self):
        """Test quadratic equation with a = 0 (degenerates to linear)"""
        # Test: 0x² + 2x + 3 = 0 -> should raise ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            my_math.quad_eq(0, 2, 3)
    
    def test_quad_eq_edge_cases(self):
        """Test edge cases for quadratic equations"""
        # Test: x² = 0 -> x = 0
        result = my_math.quad_eq(1, 0, 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0)
        
        # Test: -x² + 4 = 0 -> x = 2, x = -2
        result = my_math.quad_eq(-1, 0, 4)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0], -2.0, places=10)
        self.assertAlmostEqual(result[1], 2.0, places=10)
    
    def test_quad_eq_float_coefficients(self):
        """Test quadratic equation with float coefficients"""
        # Test: 0.5x² - 1.5x + 1 = 0 -> x = 1, x = 2
        result = my_math.quad_eq(0.5, -1.5, 1)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0], 2.0, places=10)
        self.assertAlmostEqual(result[1], 1.0, places=10)


if __name__ == "__main__":
    # Run the unit tests
    print("Running unit tests for my_math class...")
    unittest.main(verbosity=2, exit=False)

    print("\n" + "="*50)
    print("Interactive mode:")

    # Original interactive code
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