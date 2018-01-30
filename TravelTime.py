import math
import numpy as np


def destination(Po, L, V, t):
    """
    Po: point of origin. numpy array
    L: route to travel. numpy array
    V: speed in route. float
    t: time to travel in route. float
    Pu: returns destination Point
    """
    l = V * t

    absL = math.sqrt(L[0] ** 2 + L[1] ** 2)

    c = l / absL

    lvec = L * c

    Pu = Po + lvec
    return Pu

