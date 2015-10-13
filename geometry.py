from math import cos, sin, pi, radians

import numpy as np

def perpendicular_segment(a) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def segment_intersection(a1, a2, b1, b2):
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular_segment(da)
    denom = np.dot(dap, db)
    if denom == 0:
        return None
    num = np.dot(dap, dp)
    off_fact = (num / denom.astype(float))
    if off_fact < 0 or off_fact > 1.0:
        return None
    return  b1 + off_fact * db

class ZellijSector(object):
    def __init__(self, angle, r, incr):
        angle = radians(angle)

        self.angle = angle
        self.r = r
        self.unit = np.array([cos(angle), sin(angle)])
        self.normal = np.array([cos(angle + pi/2), sin(angle + pi/2)])

        self.lines = []
        for off in range(-r, r + 1, int(r/incr)):
            p = off * self.normal
            a, b = p - r * self.unit, p + r * self.unit
            self.lines.append((a, b))


class Zellij(object):
    def __init__(self, r=90, incr=4, init_angle=0):
        self.sectors = [ZellijSector(angle, r, incr) for angle in range(init_angle, init_angle + 136, int(135/3))]
        self.intersections = []

        for sector in self.sectors:
            for o_sector in self.sectors:
                if sector == o_sector:
                    continue
                collinearity = np.product([sector.unit, o_sector.unit])
                if collinearity == 0:
                    continue
                self.intersect(sector, o_sector)

    def intersect(self, sector, o_sector):
        for line in sector.lines:
            for o_line in o_sector.lines:
                intersection = segment_intersection(line[0], line[1], o_line[0], o_line[1])
                if intersection is None:
                    continue
                self.intersections.append((intersection, sector, o_sector))
