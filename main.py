import itertools

import numpy as np
import pyglet
from pyglet.gl import *
import seaborn as sns
sns.set_palette('deep')

from geometry import Zellij

class GameWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)

        # Setting up OpenGL context
        self.setup_opengl()

        # Setting the resource path
        pyglet.resource.path = ['images']
        pyglet.resource.reindex()

        # Setting-up the clock / max FPS / update event
        self.fps = 80.
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
        pyglet.clock.set_fps_limit(self.fps)

        # FPS display, for debugging purposes
        self.fps_display = pyglet.clock.ClockDisplay()

        # Zellij generator
        self.r = 100
        self.incr = 5
        self.init_angle = 0
        self.scroll_y = 0
        self.zellij = Zellij(self.r, self.incr, self.init_angle)
        self.zellij_colors = [(np.array(c) * 255).astype(int) for c in sns.color_palette()]

    def setup_opengl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glClearColor(0.2, 0.2, 0.2, 1)

    def center_coords(self, *points):
        offset = np.array([self.width / 2, self.height / 2])
        for point in points:
            yield offset + point


    def draw_line(self, a, b, color):
        a, b = self.center_coords(a, b)
        coords = tuple(itertools.chain(a.astype(int), b.astype(int)))
        color_tuple = tuple(itertools.chain(color, color))
        glLineWidth(1)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', coords),
            ('c3B', color_tuple)
        )


    def draw_quad(self, a, b, c, d, color):
        a, b, c, d = self.center_coords(a, b, c, d)
        coords = np.array(tuple(itertools.chain(a, b, c, d))).astype(int)
        color_tuple = tuple(itertools.chain(color, color, color, color))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2i', coords),
            ('c3B', color_tuple)
        )

    def draw_test(self):
        self.draw_line([10, 10], [400, 20], [200, 200, 200])
        self.draw_quad([-10, 0], [0, 10], [10, 0], [0, -10], color=[100, 220, 100])

    def draw_zellij(self):
        # Drawing sectors' background
        for sector, color in zip(self.zellij.sectors, self.zellij_colors):
            c = np.array([0, 0])
            su, sn = sector.r * sector.unit, sector.r * sector.normal
            self.draw_quad(c - su - sn,
                           c + su - sn,
                           c + su + sn,
                           c - su + sn, color=(0.6 * np.array(color) + 0.2 * 255 * np.ones(3)).astype(int))

        # Drawing sectors' lines
        for sector, color in zip(self.zellij.sectors, self.zellij_colors):
            for a, b in sector.lines:
                self.draw_line(a, b, color=(0.3 * np.array(color) + 0.2 * 255 * np.ones(3)).astype(int))

        # # Drawing intersections
        # for p, s, o_s in self.zellij.intersections:
        #     su, osu = 2 * s.unit, 2 * o_s.unit
        #     coords = [p - su - osu,
        #               p - su + osu,
        #               p + su + osu,
        #               p + su - osu]
        #     self.draw_quad(*coords, color=[80, 80, 80])


    def on_draw(self):
        self.clear()

        #self.draw_test()
        self.draw_zellij()

        self.fps_display.draw()

    def update(self, dt):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.r = max(10, int(100 + 300.0 * (self.height - y) / self.height))
        self.incr = max(1, int(5 + 10.0 * (self.width - x) / self.width))
        self.regenerate_zellij()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.scroll_y += scroll_y
        self.init_angle = int((self.scroll_y // 2) * 7.5) % 180
        self.regenerate_zellij()

    def regenerate_zellij(self):
        z = self.zellij
        if z.r == self.r and z.incr == self.incr and z.init_angle == self.init_angle:
            return
        self.zellij = Zellij(incr=self.incr, r=self.r, init_angle=self.init_angle)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

if __name__ == '__main__':
    window = GameWindow(width=1200, height=800)
    pyglet.app.run()