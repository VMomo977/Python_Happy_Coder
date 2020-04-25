import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192         # The port used by the server

"""order"""
def json_message():
    local_ip = socket.gethostbyname(socket.gethostname())

    message(generateOrder(local_ip))


def generateOrder(local_ip):
    data = {
        'local_ip': local_ip,
        'Hamburger': 2,
        'Krumpli': 2,
        'Cola': 3
    }

    json_data = json.dumps(data)

    return json_data

"""receive the menu and send the order"""
def message(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # send
        s.send('I am a customer'.encode())

        # receive
        menu = s.recv(4096)
        json_menu = json.loads(menu.decode('utf-8'))
        print("Menu: %s" % json_menu)
        # send
        # it should send the json size too
        s.sendall(data.encode())

        # receive orderNum
        orderNum = s.recv(4096)
        orderNum = orderNum.decode('utf-8')
        print('OrderNum: ', orderNum)

if __name__ == '__main__':
    json_message()
