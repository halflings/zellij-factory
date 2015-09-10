import itertools

import numpy as np
import pyglet
from pyglet.gl import *

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
        self.zellij = Zellij()
        self.zellij_colors = [[220, 100, 100], [100, 220, 100], [100, 100, 220], [220, 100, 220]]

    def setup_opengl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glClearColor(0.2, 0.2, 0.2, 1)

    def draw_line(self, a , b, color):
        coords = tuple(itertools.chain(a, b))
        color_tuple = tuple(itertools.chain(color, color))
        glLineWidth(1)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', coords),
            ('c3B', color_tuple)
        )


    def draw_quad(self, a, b, c, d, color):
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
        offset = np.array([self.width / 2, self.height / 2])
        for zellij_sector, color in zip(self.zellij.sectors, self.zellij_colors):
            for a, b in zellij_sector.lines:
                a, b = offset + a.astype(int), offset + b.astype(int)
                self.draw_line(a, b, color=color)

        for p in self.zellij.intersections:
            coords = [p - np.array([0, 4]), p - np.array([4, 0]), p + np.array([0, 4]), p + np.array([4, 0])]
            coords = map(lambda p : p + offset, coords)
            self.draw_quad(*coords, color=[220, 100, 100])

    def on_draw(self):
        self.clear()

        #self.draw_test()
        self.draw_zellij()

        self.fps_display.draw()

    def update(self, dt):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        r = int(100 + 300.0 * (self.height - y) / self.height)
        incr = int(5 + 10.0 * (self.width - x) / self.width)
        self.zellij = Zellij(incr=incr, r=r)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

if __name__ == '__main__':
    window = GameWindow(width=800, height=600)
    pyglet.app.run()