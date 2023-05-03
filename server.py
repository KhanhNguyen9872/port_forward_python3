#!/usr/bin/python3
from sys import exit
if __name__!='__main__':exit()

def get_localip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def get_publicip():
    return urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')

def random_str(length=6):
    return "".join([choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789") for i in range(length)])

def clear():
    system("cls" if osname=='nt' else "clear")
    return

def forw(source,destination,ip,port,is_a=0,soc=""):
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
    if is_a:
        try:
            soc.close()
        except:
            pass
    # except:
    #     pass
    return

def check_port(host,port):
    global ip_for_check
    print("Listening on {}:{} (2).....".format(host,port))
    try:
        soc = socket.socket()
        soc.bind((str(host),int(port)))
        soc.listen(9)
        print("Server check started!")
        while 1:
            try:
                a,b = soc.accept()
                print("Accept check: {}:{}".format(b[0],b[1]))
                string = decompress(a.recv(512)).decode()
                if string == ip_for_check[b[0]]:
                    print("Check OK: {}:{}".format(b[0],b[1]))
                    a.send(compress(b"OK!"))
                    globals()["is_start_{}_{}".format(ip_for_check[b[0]].split(":")[0],ip_for_check[b[0]].split(":")[1])]=1
                    print("check: is_start_{}_{}".format(ip_for_check[b[0]].split(":")[0],ip_for_check[b[0]].split(":")[1]))
                else:
                    a.close()
            except PermissionError as e:
                print("PermissionError: {}".format(e))
            # except OSError as e:
            #     print("OSError: {}".format(e))
    except PermissionError as e:
        print("OSError: {}".format(e))
        return
    return

def ip_forward(a,host,port,b0,b1):
    s = socket.socket()
    s.bind((str(host),int(port)))
    s.settimeout(timeout_connected)
    s.listen(9)
    while 1:
        try:
            aa,bb = s.accept()
            print("Accept: {}:{} ({}:{} -> {}:{})".format(bb[0],bb[1],host,port,b0,b1))
            aa.settimeout(timeout_connected)
            Thread(target=forw,args=(a,aa,host,port,1,s)).start()
            Thread(target=forw,args=(aa,a,host,port)).start()
        except OSError:
            if "[closed]" in str(s):
                return
            try:
                a.send(b"")
                a.send(b"")
                a.send(b"")
                print("Closed: {}:{}".format(b0,b1))
            except:
                print("Host closed: {}:{}".format(b0,b1))
                s.close()
                return
            return
    return

def start_forward(a,ip,port_rand,b0,b1):
    globals()["is_start_{}_{}".format(ip,port_rand)]=0
    print("start_forward: is_start_{}_{}".format(ip,port_rand))
    while globals()["is_start_{}_{}".format(ip,port_rand)]==0:
        sleep(1)

    # edit "0.0.0.0" to ip (below)
    Thread(target=ip_forward,args=(a,"0.0.0.0",port_rand,ip,port_rand)).start()

def run(host,port):
    global forward, ip_for_check
    print("Listening on {}:{} (1).....".format(host,port))
    try:
        soc = socket.socket()
        soc.bind((str(host),int(port)))
        soc.listen(9)
        print("Server started!")
        while 1:
            try:
                a,b = soc.accept()
                print("Accept: {}:{}".format(b[0],b[1]))
                string = decompress(a.recv(512)).decode()
                if string=="__get_ip__":
                    while 1:
                        port_rand = int(randrange(10000,40000))
                        if port_rand in forward:
                            continue
                        else:
                            try:
                                tmp_soc = socket.socket()
                                tmp_soc.bind((str(host),int(port_rand)))
                                tmp_soc.listen(9)
                                ip_for_check[b[0]]=str(public_ip)+":"+str(port_rand)
                                forward.append(port_rand)
                                tmp_soc.close()
                            except OSError:
                                continue
                        break
                    #forward[b[1]]="{}:{}".format(public_ip,port_rand)
                    print("GET IP: {}:{} -> {}:{} ({} sec)".format(b[0],b[1],public_ip,port_rand,timeout_connected))
                    a.send(compress("{}:{}".format(public_ip,port_rand).encode()))
                    Thread(target=start_forward,args=(a,public_ip,port_rand,b[0],b[1])).start()
                else:
                    a.close()
            except PermissionError as e:
                print("PermissionError: {}".format(e))
                return
            
            # except OSError as e:
            #     print("OSError: {}".format(e))
    except PermissionError as e:
        print("OSError: {}".format(e))
        return

# import
import socket
from zlib import compress,decompress
from threading import Thread
import urllib.request
from random import randrange,choice
from os import system
from os import name as osname
from time import sleep
local_ip = get_localip()
public_ip = get_publicip()
host = "0.0.0.0"
port = 12345
port_2 = 12346
#timeout_not_connect = 120
timeout_connected = 600
forward = []
ip_for_check = {}
clear()
print("Your Local IP: {}".format(local_ip))
print("Your Public IP: {}".format(public_ip))

Thread(target=check_port, args=(host,port_2)).start()
run(host,port)