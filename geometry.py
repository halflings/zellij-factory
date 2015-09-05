from math import cos, sin, pi, radians

import numpy as np

class ZellijSector(object):
    def __init__(self, angle, r, incr):
        angle = radians(angle)

        self.angle = angle
        self.r = r
        self.unit = np.array([cos(angle), sin(angle)])
        self.normal = np.array([cos(angle + pi/2), sin(angle + pi/2)])

        self.lines = []
        for off in range(-r, r + 1, incr):
            p = off * self.normal
            a, b = p - r * self.unit, p + r * self.unit
            self.lines.append((a, b))


class Zellij(object):
    def __init__(self, r=200, incr=20):
        self.sectors = [ZellijSector(angle, r, incr) for angle in range(0, 136, int(135/3))]

if __name__ == '__main__':
    z = Zellij(angle=45)

    print(z.lines)