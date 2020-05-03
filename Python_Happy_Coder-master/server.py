import socket
import json
import sys

from flask import Flask, request, abort
import functools
import time
import csv

"""create the application object"""
app = Flask(__name__)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192         # The port used by the server
BUFFER_SIZE = 4096

orderProj = []
customers = {}
sumIncome = 0
sumCustomer = 0

"""decorator to check the runtime of the decorated function"""
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter() # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter() # 2
        run_time = end_time - start_time # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

"""decorator to check the runtime of the decorated function"""
"""decorator to check that the server get wrong data"""
@timer
@app.route("/grade", methods=["POST"])
def check_jsondata(json_data, menu):

    if "local_ip" not in json_data:
        abort(400)  # stop the code, maybe this is too strong error

    try:
        if(len(json_data.keys()) < 2):
            raise ValueError("Number of keys in request can't be less than 2")
        else:
            print("Data: %s" % json_data)

            # use generator for get the cost of the order
            getCost(json_data, menu)



    except ValueError as vr:
        print('\033[91m', "Received error:",  vr , '\033[0m')

"""use generator for get the cost of the order"""
def getCost(json_data, menu):
    costs = (menu.get(key) * value for key, value in json_data.items() if menu.__contains__(key))
    ordersum = sum(costs)
    print("Cost of the order: ", ordersum)

    global sumCustomer
    global sumIncome

    sumIncome += ordersum
    sumCustomer +=1

"""customer client"""
# communicate with customerClient.py
def customerClient(conn, addr, menu):
    json_menu = json.dumps(menu)
    # send
    conn.sendall(json_menu.encode())

    # receive
    # it depends on buffer_size
    request_data = conn.recv(BUFFER_SIZE)

    # it should containt the json size too
    json_data = json.loads(request_data.decode('utf-8'))

    # decorator to check the runtime of the decorated function
    # decorator to check that the server get wrong data
    check_jsondata(json_data, menu)

    # set ordernumber
    setOrderNumber(conn, addr)

# communicate with orderNumClient.py
def setOrderNumber(conn, addr):
    print("setOrderNumber")

    data = {
        'addr': addr[1],
        'ordertype': 'order'
    }

    d = json.dumps(data).encode()
    # orderProj[0] = conn, orderProj[1] = addr
    orderProj[0].sendall(d)

    # receive addr, ordertype, orderNum
    msg = orderProj[0].recv(4096)
    msg = json.loads( msg.decode('utf-8') )
    print("OrderNum: %s" % msg)

    # send the client the orderNum
    cust_addr = msg['addr']
    cust_orderNum = str( msg['orderNum'] )
    global customers
    cust_conn = customers.get(cust_addr)
    cust_conn.send(cust_orderNum.encode())


"""server socket accept"""
def server_socket(menu):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen()
        while 1: # Accept connections from multiple clients
            print('Listening for client...')
            conn, addr = s.accept()
            print('Connection address:', addr)
            while 1: # Accept multiple messages from each client
                # receive
                conn_type = conn.recv(BUFFER_SIZE)
                conn_type = conn_type.decode('utf-8')
                print("Client: ", conn_type)
                if conn_type == 'I am a customer':
                    global customers
                    customers[addr[1]] = conn

                    customerClient(conn, addr, menu)
                elif conn_type == 'I am an order projector':
                    global orderProj
                    orderProj = [conn, addr]
                elif conn_type == 'End of the day':
                    server_exit()
                else:
                    print("Not waited client")

                break;

def load_menu(filename):
    menu = {}
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            menu[row[0]] = int(row[1])
    return menu

def print_sum():
    print('Daily income: ', sumIncome)
    print('Number of the orders: ', sumCustomer)

def server_exit():
    print_sum()
    input("Press Enter to exit...")
    sys.exit(0)

server_socket(load_menu('menu.txt'))
