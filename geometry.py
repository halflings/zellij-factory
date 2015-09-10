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
        for off in range(-r, r + 1, int(r/incr)):
            p = off * self.normal
            a, b = p - r * self.unit, p + r * self.unit
            self.lines.append((a, b))


class Zellij(object):
    def __init__(self, r=90, incr=4):
        self.sectors = [ZellijSector(angle, r, incr) for angle in range(0, 136, int(135/3))]
        self.intersections = []
        for sector in self.sectors:
            for o_sector in self.sectors:
                if sector == o_sector:
                    continue
                collinearity = np.product([sector.unit, o_sector.unit])
                if collinearity == 0:
                    continue
                for line in sector.lines:
                    for o_line in o_sector.lines:
                        delta = np.product([o_line[0] - line[0], o_sector.unit]) / collinearity
                        if delta < 0 or delta > 2 * sector.r:
                            continue
                        intersection = line[0] + delta * sector.unit
                        #print(intersection)
                        self.intersections.append(intersection)

if __name__ == '__main__':
    z = Zellij(angle=45)

    print(z.lines)