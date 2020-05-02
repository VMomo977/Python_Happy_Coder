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
        self.orderNum = 0

        # socket, thread
        self.sock = MySocket()
        Thread(target=self.setOrderNum).start()

    def setOrderNum(self):
        self.sock.send_data('I am an order projector'.encode())
        while True:
            self.orderNum += 1

            # get the customer addr, ordertype from server
            server_msg = json.loads(self.sock.get_data().decode("utf-8"))
            print("Server: %s" % server_msg)

            # create orderNum buttons
            btn =Button(
                text=str(self.orderNum),
                size_hint_y=None,
                height=40
            )

            self.scroll_grid_layout.add_widget(btn)

            # send customer addr, ordertype, orderNum to the server
            server_orderNum = {
                'addr': server_msg['addr'],
                'ordertype': 'in progress',
                'orderNum': self.orderNum
            }
            server_orderNum_msg = json.dumps(server_orderNum).encode()
            self.sock.send_data(server_orderNum_msg)

class OrderNumApp(App):
    title = "Ordernum Projector"

    def build(self):
        orderScreen = OrderNumClass()
        return orderScreen.widget_main

if __name__ == '__main__':
    OrderNumApp().run()