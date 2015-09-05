from math import cos, sin, pi, radians

import numpy as np

class ZellijSector(object):
    def __init__(self, angle, r=500, w=400, incr=20):
        angle = radians(angle)

        self.angle = angle
        self.r = r
        self.unit = np.array([cos(angle), sin(angle)])
        self.normal = np.array([cos(angle + pi/2), sin(angle + pi/2)])

        self.lines = []
        for x in range(-w, +w, incr):
            p = np.array([x, 0])
            a, b = p - r * self.unit, p + r * self.unit
            self.lines.append((a, b))


class Zellij(object):
    def __init__(self, r=500, w=400, incr=20):
        self.sectors = [ZellijSector(angle) for angle in range(0, 136, int(135/3))]

if __name__ == '__main__':
    z = Zellij(angle=45)

    print(z.lines)