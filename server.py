import socket
import json
import sys
import readFile
from decorator import timer

class ServerClass():
    def __init__(self):
        self.HOST = '127.0.0.1'  # The server's hostname or IP address
        self.PORT = 8192         # The port used by the server
        self.BUFFER_SIZE = 4096

        self.orderProj = []
        self.customers = {}
        self.sumIncome = 0
        self.sumCustomer = 0

    """decorator to check the runtime of the decorated function"""
    @timer
    def check_jsondata(self, json_data, menu):
        try:
            if "local_ip" not in json_data:
                raise ValueError("Local ip in request can not found")
        except ValueError as vr_l:
            print('\033[91m', "Received error:",  vr_l , '\033[0m')

        try:
            if(len(json_data.keys()) < 2):
                raise ValueError("Number of keys in request can't be less than 2")
            else:
                print("Orderlist from customer: %s" % json_data)

                # use generator for get the cost of the order
                self.getCost(json_data, menu)
        except ValueError as vr:
            print('\033[91m', "Received error:",  vr , '\033[0m')

    """use generator for get the cost of the order"""
    def getCost(self, json_data, menu):
        costs = (menu.get(key) * value for key, value in json_data.items() if menu.__contains__(key))
        ordersum = sum(costs)
        print("Cost of the order: ", ordersum)

        self.sumIncome += ordersum
        self.sumCustomer +=1

    """customer client"""
    # communicate with customerClient.py
    def customerClient(self, conn, addr, menu):
        json_menu = json.dumps(menu)
        # send
        conn.sendall(json_menu.encode())

        # receive
        # it depends on buffer_size
        request_data = conn.recv(self.BUFFER_SIZE)

        # it should contain the json size too
        json_data = json.loads(request_data.decode('utf-8'))

        # decorator to check the runtime of the decorated function
        # decorator to check that the server get wrong data
        self.check_jsondata(json_data, menu)

        # set ordernumber
        self.setOrderNumber(addr)

    # communicate with orderNumClient.py
    def setOrderNumber(self, addr):
        data = {
            'addr0': addr[0],
            'addr1': addr[1],
            'ordertype': 'order'
        }

        d = json.dumps(data).encode()
        # orderProj[0] = conn, orderProj[1] = addr
        self.orderProj[0].sendall(d)

        # receive addr, ordertype, orderNum
        msg = self.orderProj[0].recv(4096)
        msg = json.loads( msg.decode('utf-8') )
        print("OrderNum: %s" % msg)

        # send the client the orderNum
        cust_addr0 = msg['addr0']
        cust_addr1 = msg['addr1']
        cust_orderNum = str( msg['orderNum'] )

        # if we use only own computer for test, that the addr1 (id) is the distinguishable data, not the addr0
        cust_conn = self.customers.get(cust_addr0).get(cust_addr1)
        cust_conn.send(cust_orderNum.encode())


    """server socket accept"""
    def server_socket(self, menu):
        print(menu)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST,self.PORT))
            s.listen()
            while 1: # Accept connections from multiple clients
                print('\nListening for client...')
                conn, addr = s.accept()
                print('\nConnection address:', addr)
                while 1: # Accept multiple messages from each client
                    # receive
                    conn_type = conn.recv(self.BUFFER_SIZE)
                    conn_type = conn_type.decode('utf-8')
                    print("Client: ", conn_type)
                    if conn_type == 'I am a customer':
                        # if we use only own computer for test, that the addr1 (id) is the distinguishable data, not the addr0
                        tmp = {}
                        tmp[addr[1]] = conn
                        self.customers[addr[0]] = tmp

                        self.customerClient(conn, addr, menu)
                    elif conn_type == 'I am an order projector':
                        self.orderProj = [conn, addr]
                    elif conn_type == 'End of the day':
                        self.server_exit()
                    else:
                        print("Not waited client")

                    break;

    def print_sum(self):
        print('\nDaily income: ', self.sumIncome)
        print('Number of the orders: ', self.sumCustomer)

    def server_exit(self):
        self.print_sum()
        input("\nPress Enter to exit...")
        sys.exit(0)

if __name__ == '__main__':
    server1 = ServerClass()
    server1.server_socket(readFile.load_menu('menu.txt'))
