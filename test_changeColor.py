from unittest import TestCase

from kivy.tests.common import GraphicUnitTest, UnitTestTouch


class TesChangeColor(GraphicUnitTest):

    def test_changeColor(self):
        from kivy.uix.button import Button

        # with GraphicUnitTest.render() you basically do this:
        # runTouchApp(Button()) + some setup before
        button = Button(background_color=[0.95, 0.45, 0.20, 1.0])

        self.render(button)

        # get your Window instance safely
        from kivy.base import EventLoop
        EventLoop.ensure_window()
        window = EventLoop.window

        touch = UnitTestTouch(
            *[s / 2.0 for s in window.size]
        )

        # bind something to test the touch with
        button.bind(
            on_press=lambda instance: setattr(
                instance, 'background_color',  [0.0, 1.0, 0.0, 1.0]
            )
        )
        # then let's touch the Window's center
        touch.touch_down()
        touch.touch_up()
        self.assertEqual(button.background_color, [0.0, 1.0, 0.0, 1.0])
