import socket
from scapy.all import ARP, Ether, srp

while True:
    addr = input("Укажите режим all[0]/one[1] (По умолчанию all): ")
    if addr == "" or addr == "all" or addr == "0":
        hostname = socket.gethostname()
        print(hostname)
        if hostname:
            target_ip = socket.gethostbyname(hostname) + "/24"
        else:
            target_ip = "127.0.0.1/24"
        print(target_ip)
        result = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=3, verbose=False)[0]
        devices = []
        for _, received in result:
            devices.append({'ip': received.psrc,'mac': received.hwsrc})
        break
    elif addr == "one" or addr == "1":
        target_ip = input("Укажите конкретный адрес: ")
        result = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=3, verbose=False)[0]
        devices = []
        for _, received in result:
            devices.append({'ip': received.psrc,'mac': received.hwsrc})
        print(devices)
        break
    else:
        print("Непонятная команда: ", addr)
        while True:
            addr = input("Продолжить? yes[1]/no[0]: ")
            if addr == "yes" or addr == "1":
                continue
            elif addr == "no" or addr == "0":
                exit()
            else:
                print("Можно больше не ошибаться?")

print("-" * 50)
server = socket.socket()
port = 12345
pull = []

for device in devices:
    dev = device['ip']
    try:
        # print(dev, port)
        server.connect((dev, port))
        print("Server connection: ", server)
        message = "OK"
        server.send(message.encode())
        data = server.recv(1024)
        message = (data.decode())
        data = list(message.split(";"))
        server.close()
        pull.append(data)
    except:
        print("Server no connect: ",dev, " ", server)
print(pull)