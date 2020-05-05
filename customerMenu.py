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

class CustomerClass():

    def __init__(self, **kwargs):
        super(CustomerClass,self).__init__(**kwargs)
        """Widgets"""
        # set layouts, widgets
        self.widget_main = Widget()

        self.scroll_grid_layout = ScrollGridLayout()

        self.scroll_grid_layout.bind(minimum_height=self.scroll_grid_layout.setter('height'))

        self.scrollview = ScrollView(effect_cls='ScrollEffect', size_hint=(1, None), size=(Window.width, Window.height))

        self.scrollview.add_widget(self.scroll_grid_layout)

        self.widget_main.add_widget(self.scrollview)

        """server-client thread"""
        Thread(target=self.connectToTheServer).start()


    def addProduct(self, menu):

        for keys in menu.keys():
            btn =Button(
                text=keys,
                size_hint_y=None,
                height=40
            )
            self.scroll_grid_layout.add_widget(btn)

    """order"""
    def generateOrder(self, sock):
        local_ip = sock.local_ip
        order_list = {
            'local_ip': local_ip,
            'Hamburger': 2,
            'Krumpli': 2,
            'Cola': 3
        }
        json_data = json.dumps(order_list)
        return json_data

    def connectToTheServer(self):
        sock = MySocket()

        sock.send_data('I am a customer'.encode())

        """receive menu from server"""
        menu = json.loads(sock.get_data().decode("utf-8"))
        print("Server send the menu: %s" % menu)

        """Menu GUI"""
        self.addProduct(menu)

        """send the order list with food, drink"""
        # it should send the json size too
        data = self.generateOrder(sock)
        sock.send_data(data.encode())

        """receive orderNum"""
        orderNum = sock.get_data().decode('utf-8')
        print('OrderNum: ', orderNum)


class CustomerApp(App):
    title = "Customer Menu"

    def build(self):
        customerScreen = CustomerClass()
        return customerScreen.widget_main

if __name__ == '__main__':
    CustomerApp().run()