import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown

from orderNumClient import *
from threading import Thread


class CustomDropDown(DropDown):
    orderNum = 0

    def __init__(self, **kwargs):
        super(CustomDropDown,self).__init__(**kwargs)

        self.sock = MySocket()
        Thread(target=self.setOrderNum).start()

    def setOrderNum(self):
        self.sock.send_data('I am an order projector'.encode())
        while True:
            self.orderNum += 1

            # get the customer addr, ordertype from server
            server_msg = json.loads(self.sock.get_data().decode("utf-8"))
            print("Server: %s" % server_msg)

            # create button for orderNum projection
            btn = Button(text='Order %d' % (self.orderNum), size_hint_y=None, height=44)
            print("Hej")
            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: self.select(btn.text))

            # then add the button inside the dropdown
            self.add_widget(btn)

            # send customer addr, ordertype, orderNum to the server
            server_orderNum = {
                'addr': server_msg['addr'],
                'ordertype': 'in progress',
                'orderNum': self.orderNum
            }
            server_orderNum_msg = json.dumps(server_orderNum).encode()
            self.sock.send_data(server_orderNum_msg)

class Notes(Screen):
    pass

class MyScreenManager(ScreenManager):

    def Run_Draws_Test(self, value):
        print(value)


class OrderNumApp(App):
    title = "Kivy Drop-Down List Demo"

    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    OrderNumApp().run()