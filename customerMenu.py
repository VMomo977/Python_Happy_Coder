import json
from typing import Any

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from functools import partial

from customerClient import *
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

        self.order_list = {}
        self.finish_order_list = False

    def addToOrderList(self, instance):
        # 'Cola: 300': 1 -> cut the price
        key = instance.text.split(':')[0]
        if self.order_list.__contains__(key):
            self.order_list[key] += 1
            print("Buy the customer: ", key, " item: ",self.order_list[key])
        else:
            self.order_list[key] = 1
            print("Buy the customer: ", key, " item: ", self.order_list[key])


    def addProduct(self, menu, sock):

        for key in menu.keys():

            product =Button(
                text=key + ": " + str(menu[key]),
                size_hint_y=None,
                height=40
            )
            product.bind(on_press=self.addToOrderList)
            self.scroll_grid_layout.add_widget(product)

        send_order_list = Button(
            text="Send the order list",
            size_hint_y=None,
            height=40
        )

        send_order_list.bind(on_press= lambda x : setattr(self, 'finish_order_list', True))

        self.scroll_grid_layout.add_widget(send_order_list)

    """order"""

    def generateOrder(self, local_ip):

        """
            order_list = {
            'local_ip': local_ip,
            'Hamburger': 2,
            'Krumpli': 2,
            'Cola': 3
        }
        """
        self.order_list['local_ip'] = local_ip

        print("Orderlist: %s"% self.order_list)
        json_data = json.dumps(self.order_list)
        return json_data

    def sendOrder(self, sock, data):
        sock.send_data(data.encode())

        """receive orderNum"""
        orderNum = sock.get_data().decode('utf-8')
        print('OrderNum: ', orderNum)

        App.get_running_app().stop()

def connectToTheServer(screen):
    sock = MySocket()

    sock.send_data('I am a customer'.encode())

    """receive menu from server"""
    menu = json.loads(sock.get_data().decode("utf-8"))
    print("Server send the menu: %s" % menu)

    """Menu GUI"""
    screen.addProduct(menu, sock)
    while(screen.finish_order_list != True):
        tmp = ("Waiting") #it need some sleeping
        #print("Wait the client finish the order list")
    print("The client will send the order to the server")
    json_data = screen.generateOrder(sock.local_ip)
    screen.sendOrder(sock, json_data)

class CustomerApp(App):
    title = "Customer Menu"

    def build(self):
        customerScreen = CustomerClass()

        """server-client thread"""
        Thread(target=connectToTheServer, args=[customerScreen]).start()

        return customerScreen.widget_main

if __name__ == '__main__':

    CustomerApp().run()