import json

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.scrollview import ScrollView

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

    def __init__(self, kitchen, **kwargs):
        self.kitchen = kitchen
        extraSpace = 40 if kitchen else 0

        super(OrderNumClass,self).__init__(**kwargs)

        # set layouts, widgets
        self.widget_main = Screen(name= 'kitchen' if kitchen else 'order')

        self.scroll_grid_layout = ScrollGridLayout()

        self.scroll_grid_layout.bind(minimum_height=self.scroll_grid_layout.setter('height'))

        self.scrollview = ScrollView(effect_cls='ScrollEffect', size_hint=(1, None), size=(Window.width, Window.height-extraSpace))

        self.scrollview.add_widget(self.scroll_grid_layout)

        if kitchen:
            box_layout = BoxLayout(orientation="vertical")
            exitbtn = Button(
                text='End Day',
                size_hint_y=None,
                height=40,
                on_press=self.exit_server
            )
            box_layout.add_widget(exitbtn)
            box_layout.add_widget(self.scrollview)

        self.widget_main.add_widget(box_layout if kitchen else self.scrollview)


    def exit_server(self, *args):
        sock = MySocket()
        sock.send_data('End of the day'.encode())
        App.get_running_app().stop()

    def changeColor(self, orderNum):
        for screen in createButtons:
            for button in screen.scroll_grid_layout.children:
                if button.text == str(orderNum):
                    button.background_color= (0.0, 1.0, 0.0, 1.0)
                    # idozitovel gomblevetel

    def setOrderNum(self, orderNum):
        # create orderNum buttons
        btn =Button(
            text=str(orderNum),
            size_hint_y=None,
            height=40,
            on_press= lambda _: self.changeColor(orderNum),
            background_color=[0.95, 0.45, 0.20, 1.0]
        )
        self.scroll_grid_layout.add_widget(btn)

def connectToServer():

    sock = MySocket()
    orderNum = 0

    sock.send_data('I am an order projector'.encode())
    while True:
        orderNum += 1

        # get the customer addr, ordertype from server
        server_msg = json.loads(sock.get_data().decode("utf-8"))
        print("Server: %s" % server_msg)

        for createButton in createButtons:
            createButton.setOrderNum(orderNum)

        # send customer addr, ordertype, orderNum to the server
        server_orderNum = {
            'addr': server_msg['addr'],
            'ordertype': 'in progress',
            'orderNum': orderNum
        }
        server_orderNum_msg = json.dumps(server_orderNum).encode()
        sock.send_data(server_orderNum_msg)

class OrderNumApp(App):
    title = "Ordernum Projector"
    sm = None
    kitchen = False

    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        orderScreen = OrderNumClass(False)
        kitchenScreen = OrderNumClass(True)

        sm.add_widget(orderScreen.widget_main)
        sm.add_widget(kitchenScreen.widget_main)

        createButtons.append(orderScreen)
        createButtons.append(kitchenScreen)

        Window.bind(on_key_up=self.switch)
        self.sm = sm

        return sm

    #window change
    def switch(self, window, key_code, *args):
        if key_code != 13:
            return
        self.sm.current= self.sm.next()

        #window name change
        Window.set_title('Kitchen Projector' if self.sm.current == 'kitchen' else 'Ordernum Projector')


if __name__ == '__main__':

    createButtons = []

    Thread(target=connectToServer).start()

    OrderNumApp().run()
