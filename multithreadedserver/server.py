import socket, webbrowser, base64, random, json
from string import ascii_letters
from prettytable import PrettyTable


class Server:
    DISCONNECT = '!DISCONNECT'
    connList = []
    ipList = []

    def __init__(self, port, ip):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def show_connections(self):
        table = PrettyTable()
        numbers = [i for i in range(len(self.ipList))]
        table.add_column('No.', numbers)
        table.add_column('IPS', [i[0] for i in self.ipList])
        table.add_column('PORTS', [i[1] for i in self.ipList])
        return table


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

    def exit_all_connections(self):
        for i in self.connList:
            print(i)
            # self.conn_session = i
            self.sender(self.DISCONNECT, i)