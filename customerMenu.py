import json
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from orderNumClient import *
from threading import Thread

class ScrollGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ScrollGridLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y=None
        self.height=self.minimum_height
        self.cols=2

class OrderNumClass():
    orderNum = 0

    # set layouts, widgets
    widget_main = Widget()

    scroll_grid_layout =  ScrollGridLayout()

    scroll_grid_layout.bind(minimum_height=scroll_grid_layout.setter('height'))

    scrollview = ScrollView(effect_cls='ScrollEffect', size_hint=(1, None), size=(Window.width, Window.height))

    scrollview.add_widget(scroll_grid_layout)

    widget_main.add_widget(scrollview)

    def __init__(self, **kwargs):
        super(OrderNumClass,self).__init__(**kwargs)
        self.menu = {'Hamburger': 400, 'Krumpli': 300, 'Cola': 300}
        self.addProduct(self.menu)

    def addProduct(self, menu):

        for keys in menu.keys():
            btn =Button(
                text=keys,
                size_hint_y=None,
                height=40
            )
            self.scroll_grid_layout.add_widget(btn)


class OrderNumApp(App):
    title = "Ordernum Projector"

    def build(self):
        orderScreen = OrderNumClass()
        return orderScreen.widget_main

if __name__ == '__main__':
    OrderNumApp().run()