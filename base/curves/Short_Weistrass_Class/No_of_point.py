import numpy as np
from datetime import datetime
import random
from .Inverse_mod import inverse_mod

from .Common import *


def Num_Points(a,b,p):
    print(f"Called with a={a}, d={b}, p={p}")
    if p<99999:
        array = generatePointsUpto99999(a,b,p)
        N= len(array[0])+1
    else:
        array = generatePoints(a,b,p)
        print(len(array[0]))
        # exit()
        N = func_no_of_generator_point(a,b,p,array)
    print(N)
    return N

def generatePointsUpto99999(a, d, p, start=0):
  print(f"**** generatePointsUpto99999 *****")
  #Creating the output file
  x_array = []
  y_array = []

  # $$$
  if start > p:
    start = 0

  # take at max 1000 points
  for x in range(start,  p):
      fx = ((x*x*x)+(a*x)+d)%p   #finding values of y^2 mod p for every integer value of x in range
      if(isResidue(fx, p) or fx == 0):
        # 4k+3 form
        if((p-3)%4 == 0):
          y = pow(fx, (p+1)/4, p)   #euler's method
        # 4k+1 form
        else:
          y = tonelli_shanks(fx,p)   #Tonneli-Shank's method

        x_array.append(x)
        y_array.append(y)
        if fx != 0:
          x_array.append(x)
          y_array.append(p-y)
  return (x_array,y_array)

def func_no_of_generator_point(a,b,p,array):
    print(f"**** Func_no_of_generator_point *****")
    lo = int(p + 1 - 2*(p**0.5))
    hi = int(p + 1 + 2*(p**0.5))
    print(" before tinycurve assigned")
    tinycurve = No_of_point(p,a,b,len(array[0])+1)


    set_n = set()
    no_of_points = lo

    maxi = 0
    for t in range(1, 10):
        # Ensure unique random index
        n = random.randint(0, len(array[0]) - 1)
        set_n.add(n)
        while n in set_n:
            set_n.add(n)
            n = random.randint(0, len(array[0]) - 1)

        i, j = array[0][n], array[1][n]
        # elements = set()
        # elements.add((i,j))
        # print("check 1")
        # exit()
        count = lo
        # flaf = False
        for k in range( lo, hi):
            result = tinycurve.mult(k, (i, j))
            result2 = tinycurve.mult(k+1, (i, j))
            if result == None and result2==(i,j):
                no_of_points = max(no_of_points, count)
                # if result == None:
                #     no_of_points+=1
                break  # Stop checking further for this point
            count+=1
    print(no_of_points)
    return no_of_points

class No_of_point:
    """An elliptic curve over a prime field.

    The field is specified by the parameter 'p'.
    The curve coefficients are 'a' and 'b'.
    The base point of the cyclic subgroup is 'g'.
    The order of the subgroup is 'n'.
    """

    def __init__(self, p, a, b, n):
        print(f"**** No_of_point *****")
        self.p = p
        self.a = a
        self.b = b
        self.n = n

        assert pow(2, p - 1, p) == 1
        # assert (4 * a * a * a + 27 * b * b) % p != 0
        # assert self.is_on_curve(g)
        # assert self.mult(n, g) is None

    def is_on_curve(self, point):
        """Checks whether the given point lies on the elliptic curve."""
        if point is None:
            return True

        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    def add(self, point1, point2):
        """Returns the result of point1 + point2 according to the group law."""
        # assert self.is_on_curve(point1)
        # assert self.is_on_curve(point2)

        if point1 is None:
            return point2
        if point2 is None:
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            # print("this is first mark")
            if y1==0:
                return None
            m = (3 * x1 * x1 + self.a) * inverse_mod(2 * y1, self.p)
        else:
            # print("this is second mark")
            m = (y1 - y2) * inverse_mod(x1 - x2, self.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % self.p,
                  -y3 % self.p)

        # assert self.is_on_curve(result)

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
        if self.n >0 :
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
