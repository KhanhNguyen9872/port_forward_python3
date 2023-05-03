#!/usr/bin/python3
from sys import exit
if __name__!='__main__':exit()
import socket
from zlib import decompress, compress
from threading import Thread
def forward(source,destination,ip,port):
    try:
        string = " "
        while string:
            string = source.recv(65535)
            if string:
                destination.sendall(string)
            else:
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_WR)
                break
    except TimeoutError:
        print(">> Timeout: Port {} from {}".format(str(port),str(ip)))
    except ConnectionAbortedError:
        print(">> Aborted connection: Port {} from {}".format(str(port),str(ip)))
    except ConnectionResetError:
        print(">> Close connection: Port {} from {}".format(str(port),str(ip)))
    except ConnectionRefusedError:
        print(">> Connection refused: Port {} from {}".format(str(port),str(ip)))
    except OSError:
        pass
    return

def web_getip():
    global ip
    soc1 = socket.socket()
    soc1.bind(("127.0.0.1",4040))
    soc1.listen(9)
    while 1:
        aa,bb = soc1.accept()
        aa.recv(1024)
        aa.send(str("HTTP/1.0 200 OK\nContent-Type: text/html\n\n"+ip).encode())
        aa.close()

while 1:
    try:
        ip=str(input("IP [127.0.0.1]: "))
        port=int(input("Port [1-65535]: "))
        if port<1 or port>65535:
            continue
        tmp=ip.split(".")
        if len(tmp)!=4:continue
        tmp=[int(x) for x in tmp]
        break
    except ValueError:
        continue
host_server = "127.0.0.1"
port_server_1 = 12345
port_server_2 = 12346
soc = socket.socket()
soc.connect((str(host_server),int(port_server_1)))
print(host_server)
print(port_server_1)
soc.send(compress(b"__get_ip__"))
ip = str(decompress(soc.recv(512)).decode())
try:
	if len(ip.split(":")[0].split("."))!=4 or int(ip.split(":")[1])>65535 or int(ip.split(":")[1])<1 or ":" not in ip:
		int("a")
except ValueError:
	soc.close()
	print("Server Error!")
	exit()
soc2 = socket.socket()
soc2.connect((host_server,port_server_2))
soc2.send(compress(ip.encode()))
if decompress(soc2.recv(512)).decode()!="OK!":
	soc2.close()
	print("Server Error!")
	exit()
print("ok2")
Thread(target=web_getip,args=()).start()
print("WEB IP Forward: http://127.0.0.1:4040")
print("IP Forward: {}".format(ip))
while 1:
#     a,b = soc.accept()
#     try:
#         des = socket.socket()
#         des.connect((str(ip),int(port)))
#     except KeyboardInterrupt:
        pass
#     Thread(target=forward,args=(soc,des,b[0],b[1])).start()
#     Thread(target=forward,args=(des,soc,b[0],b[1])).start()
