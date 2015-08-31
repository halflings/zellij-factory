import pyglet
from pyglet.gl import *

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

    def setup_opengl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.2, 0.2, 0.2, 1)

    def draw_test(self):
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 0, 2, 3],
            ('v2i', (100, 100,
                     300, 100,
                     300, 300,
                     100, 300)),
            ('c3B', (255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0))
        )

    def on_draw(self):
        self.clear()

        self.draw_test()

        self.fps_display.draw()

    def update(self, dt):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

if __name__ == '__main__':
    window = GameWindow(width=800, height=600)
    pyglet.app.run()