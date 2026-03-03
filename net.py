import socket
from time import time
from scapy.all import srp
from scapy.layers.l2 import ARP, Ether
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

def dev_null(console:bool): 
    def print_z(*str):
        pass

    if console:
        return print_z
    else:
        return print

# Таймауты
# REQUEST_TIMEOUT = 10
# MAX_WORKERS = 10  # Максимум 10 параллельных запросов
def target_device(target_ip):
    result = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=3, verbose=False)[0]
    devices = []
    for _, received in result:
        if received.psrc == socket.gethostbyname(socket.gethostname()):
            continue
        devices.append({'ip': received.psrc,'mac': received.hwsrc})
    return devices

# Укажите ваш диапазон сети (например, 192.168.1.0/24)
def get_local_ip(console:bool):
    while True:
        if console:
            addr = ""
        else:
            addr = input("Укажите режим all[1/Все]/one[2/Один]/exit[0/e/Выход] (По умолчанию all): ")
        if addr == "exit" or addr == "0" or addr == "e" or addr == "Выход":
            exit()
        elif addr == "" or addr == "all" or addr == "1":
            hostname = socket.gethostname()
            if hostname:
                target_ip = socket.gethostbyname(hostname) + "/24"
            else:
                target_ip = "127.0.0.1/24"
            return target_device(target_ip)
        elif addr == "one" or addr == "2":
            target_ip = input("Укажите конкретный адрес: ")
            return target_device(target_ip)
        else:
            print("Непонятная команда: ", addr)
            bobl = True
            while bobl:
                addr = input("Продолжить? yes[1]/no[0]: ")
                if addr == "yes" or addr == "1":
                    bobl = False
                elif addr == "no" or addr == "0":
                    exit()
                else:
                    print("Можно больше не ошибаться?")

def server_thread(dev: str):
    server = socket.socket()
    port = 12345
    server.settimeout(REQUEST_TIMEOUT)
    result = []
    try:
        server.connect((dev, port))
        print("Успешно: ",dev)
        message = "OK"
        server.send(message.encode())
        data = server.recv(1024)
        result = list(data.decode().split(";"))
    except socket.timeout:
        print(f"Ошибка соединения: {dev}, таймаут!")
    except socket.error as e:
        print(f"Ошибка соединения: {dev}, {e}")
    finally:
        server.close()

    return result

def request_logging(urls: List[str]) -> List[List[str]]:
    """
    Многопоточный опрос списка URL с ограничением числа потоков.
    Возвращает список результатов.
    """
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Отправляем все задачи
        future_to_url = {executor.submit(server_thread, url): url for url in urls}

        # Собираем результаты по мере завершения
        for future in as_completed(future_to_url):
            result = future.result()
            if result != []:
                results.append(result)
    return results

def main(console:bool=True, timeout:int=10, max:int=10):
    global REQUEST_TIMEOUT, MAX_WORKERS, print
    REQUEST_TIMEOUT = timeout   # Таймауты
    MAX_WORKERS = max           # Максимум параллельных запросов
    device = []
    print = dev_null(console)
    devices = get_local_ip(console)    
    for dev in devices:
        device.append(dev['ip'])
    print("-" * 50)
    print(f"Запуск опроса {len(device)} клиентов с макс. {MAX_WORKERS} потоками...\n")

    start = time()
    results = request_logging(device)
    duration = time() - start

    print(f"\nГотово за {duration:.2f} секунд")
    # print(f"Результат:\n{results}")
    return results

if __name__ == "__main__":
    print(f"Результат:\n{main(console=False)}")
