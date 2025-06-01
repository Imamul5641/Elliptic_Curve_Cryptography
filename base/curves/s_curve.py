from .Short_Weistrass_Class.No_of_point import *
from .Short_Weistrass_Class.Generator_points import *
from .Short_Weistrass_Class.Points_on_curve import *
from .Short_Weistrass_Class.Order_of_Point import *  # Compute_order
from .Short_Weistrass_Class.Common import *  # Compute_order

def num_points(a,b,p):
    return Num_Points(a, b, p)

def generator_points(a, b, p, N, array):
    return points(a, b, p, N, array)

def points_on_curve(a, b, p, start):
    return generatePoints(a, b, p, start)

def addpoints(a, b, p, point1, point2, no_of_points):
    tinycurve = No_of_point(p, a, b, no_of_points)
    res = tinycurve.add(point1, point2)
    if res==None:
        print("-*-*-*-*-*-*-*Inverse does not exist, please change the point!!*-*-*-*-*-*-*-")
        return (0, -1)
    return res

def substractpoints(a, b, p, point1, point2, no_of_points):
    p3 = (point2[0], -1 * point2[1])
    return addpoints(a, b, p, point1, p3, no_of_points)

def doublepoint(a, b, p, point1, no_of_points):
    return addpoints(a, b, p, point1, point1, no_of_points)

def multiplypoint(a, b, p, point1, scalar, no_of_points):
    tinycurve = No_of_point(p, a, b, no_of_points)
    res = tinycurve.mult(scalar, point1 )
    if res==None:
        print("-*-*-*-*-*-*-*Inverse does not exist, please change the point!!*-*-*-*-*-*-*-")
        return (0, -1)
    return res

def order_of_point(a, b, p, point, no_of_point):
    try:
        tinycurve = EllipticCurve(p, a, b, point, n=no_of_point)
        if p<99:
            xp, yp = point
            n = point_order(tinycurve, xp, yp)
            return (n, -2)
        else:
            n = compute_order(tinycurve, point, no_of_point)
            return (n, -2)
    except:
        return (1, -1)