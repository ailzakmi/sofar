import socket
from scapy.all import srp
from scapy.layers.l2 import ARP, Ether
from tkinter.messagebox import showerror
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

def open_error(mess="Сообщение об ошибке", *, error=None): 
    if error != None:
        mess = error
    showerror(title="Ошибка", message=mess, default="ok")

def target_device(target_ip):
    devices = []
    try:
        result = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=3, verbose=False)[0]
        for _, received in result:
            if received.psrc == socket.gethostbyname(socket.gethostname()):
                continue
            devices.append({'ip': received.psrc,'mac': received.hwsrc})
    except Exception as e:
        open_error(error=e)
    return devices

# Укажите ваш диапазон сети (например, 192.168.1.0/24)
def get_local_ip():
    hostname = socket.gethostname()
    if hostname:
        target_ip = socket.gethostbyname(hostname) + "/24"
    else:
        target_ip = "127.0.0.1/24"
    return target_device(target_ip)

def server_thread(dev: str):
    server = socket.socket()
    port = 12345
    server.settimeout(REQUEST_TIMEOUT)
    result = []
    try:
        server.connect((dev, port))
        message = "OK"
        server.send(message.encode())
        data = server.recv(1024)
        result = list(data.decode().split(";"))
    except socket.timeout:
        pass
    except socket.error as e:
        pass
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

def main(timeout:int=10, max:int=10):
    global REQUEST_TIMEOUT, MAX_WORKERS
    REQUEST_TIMEOUT = timeout   # Таймауты
    MAX_WORKERS = max           # Максимум параллельных запросов
    device = []
    devices = get_local_ip()    
    for dev in devices:
        device.append(dev['ip'])
    
    results = request_logging(device)
    return results

if __name__ == "__main__":
    print(f"Результат:\n{main()}")
