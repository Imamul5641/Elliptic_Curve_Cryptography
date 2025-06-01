from .Inverse_mod import inverse_mod
from .Order_of_Point import *  # Compute_order
import math
from functools import reduce

class EllipticCurve:
    """An elliptic curve over a prime field.

    The field is specified by the parameter 'p'.
    The curve coefficients are 'a' and 'b'.
    The base point of the cyclic subgroup is 'g'.
    The order of the subgroup is 'n'.
    """

    def __init__(self, p, a, b, g, n):
        self.p = p
        self.a = a
        self.b = b
        self.g = g
        self.n = n
        # print(f"**** Elliptic curve *****")

        assert pow(2, p - 1, p) == 1
        # assert (4 * a * a * a + 27 * b * b) % p != 0
        assert self.mult(n, g) is None

    def is_on_curve(self, point):
        """Checks whether the given point lies on the elliptic curve."""
        if point is None:
            return True

        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    def add(self, point1, point2):
        """Returns the result of point1 + point2 according to the group law."""
        assert self.is_on_curve(point1)
        assert self.is_on_curve(point2)

        if point1 is None:
            return point2
        if point2 is None:
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            if y1==0:
                return None
            m = (3 * x1 * x1 + self.a) * inverse_mod(2 * y1, self.p)
        else:
            m = (y1 - y2) * inverse_mod(x1 - x2, self.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % self.p,
                  -y3 % self.p)

        assert self.is_on_curve(result)

        return result

    def double(self, point):
        """Returns 2 * point."""
        return self.add(point, point)

    def neg(self, point):
        """Returns -point."""
        if point is None:
            return None

        x, y = point
        result = x, -y % self.p

        assert self.is_on_curve(result)

        return result

    def mult(self, n, point):
        """Returns n * point computed using the double and add algorithm."""
        if n % self.n == 0 or point is None:
            return None

        if n < 0:
            return self.neg(self.mult(-n, point))

        result = None
        addend = point

        while n:
            if n & 1:
                result = self.add(result, addend)
            addend = self.double(addend)
            n >>= 1

        return result

    def __str__(self):
        a = abs(self.a)
        b = abs(self.b)
        a_sign = '-' if self.a < 0 else '+'
        b_sign = '-' if self.b < 0 else '+'

        return 'y^2 = (x^3 {} {}x {} {}) mod {}'.format(
            a_sign, a, b_sign, b, self.p)


def points(a, b, p, N, array):
    count = 0
    result = [[],[]]
    for i, j in zip(array[0], array[1]):
        tinycurve = EllipticCurve(p, a, b, g=(i, j), n=N, )

        try:
            # Compute its order
            if p<99:
                n = point_order(tinycurve, i, j)
            else:
                n = compute_order(tinycurve, (i, j), N)
            if n == N:
                print(f"({i},{j}) is a generator")
                result[0].append(i)
                result[1].append(j)
                count += 1
        except:
            continue
    print(f"Total no of generator points {count}")
    return result