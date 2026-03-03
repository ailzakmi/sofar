import socket
import requests
import uuid
import speedtest
import psutil
import netifaces
from pythonping import ping as python_ping
import time
import os

# --- Утилитарные функции ---

def get_size(bytes_count):
    """
    Преобразует байты в удобочитаемый формат (B, KB, MB, GB, TB).
    """
    if not isinstance(bytes_count, (int, float)) or bytes_count is None:
        return "N/A"
        
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"

def format_report(data, target_host):
    """
    Форматирует все собранные данные в одну строку для вывода в файл и консоль.
    """
    # Добавляем метку времени начала отчета
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = []
    report_lines.append("="*50)
    report_lines.append("           СВОДНАЯ ИНФОРМАЦИЯ О СЕТИ")
    report_lines.append("="*50)
    report_lines.append(f"Дата и время отчета: {timestamp}")
    report_lines.append("-" * 30)
    
    # Блок 1: Системная информация
    report_lines.append("🖥️  Система:")
    report_lines.append(f"  Имя компьютера: {data.get('hostname', 'N/A')}")
    report_lines.append(f"  Сетевой адаптер: {data.get('interface_name', 'N/A')}")
    report_lines.append(f"  MAC-адрес: {data.get('mac_address', 'N/A')}")
    report_lines.append("-" * 30)
    
    # Блок 2: IP-адреса и шлюз
    report_lines.append(f"🌐 IP-адреса:")
    report_lines.append(f"  Внутренний IP: {data.get('local_ip', 'N/A')}")
    report_lines.append(f"  IP шлюза (роутера): {data.get('gateway_ip', 'N/A')}")
    report_lines.append(f"  Внешний IP: {data.get('external_ip', 'N/A')}")
    report_lines.append("-" * 30)

    # Блок 3: Объем данных
    report_lines.append(f"📊 Общий объем данных (с момента загрузки ОС):")
    report_lines.append(f"  Отправлено: {get_size(data.get('total_sent'))}")
    report_lines.append(f"  Получено: {get_size(data.get('total_recv'))}")
    report_lines.append("-" * 30)
    
    # Блок 4: Пинг
    report_lines.append(f"⏱️  Пинг и потеря пакетов:")
    
    # Пинг до шлюза
    report_lines.append(f"  - До шлюза ({data.get('gateway_ip', 'N/A')}):")
    ping_gw = data.get('ping_gateway_ms')
    loss_gw = data.get('loss_gateway_percent')
    if ping_gw is not None:
        report_lines.append(f"    Средний пинг: {ping_gw:.2f} мс")
        report_lines.append(f"    Потеря пакетов: {loss_gw:.2f}%")
    else:
        report_lines.append("    Не удалось проверить.")
        
    # Пинг до ya.ru
    report_lines.append(f"  - До {target_host}:")
    ping_ext = data.get('ping_ya_ru_ms')
    loss_ext = data.get('loss_ya_ru_percent')
    if ping_ext is not None:
        report_lines.append(f"    Средний пинг: {ping_ext:.2f} мс")
        report_lines.append(f"    Потеря пакетов: {loss_ext:.2f}%")
    else:
        report_lines.append("    Не удалось проверить (проверьте подключение к Интернету).")
    report_lines.append("-" * 30)
    
    # Блок 5: Скорость
    report_lines.append(f"📶 Скорость Интернета (Speedtest):")
    dl_speed = data.get('download_speed_mbps')
    ul_speed = data.get('upload_speed_mbps')
    
    if dl_speed is not None:
        report_lines.append(f"  Скорость загрузки: {dl_speed:.2f} Мбит/с")
        report_lines.append(f"  Скорость выгрузки: {ul_speed:.2f} Мбит/с")
        report_lines.append(f"  Сервер: {data.get('server_name')} ({data.get('server_location')})")
        report_lines.append(f"  Задержка до сервера: {data.get('server_latency'):.2f} мс")
    else:
        report_lines.append("  Тестирование скорости не было выполнено или завершилось ошибкой.")

    report_lines.append("="*50)
    
    return "\n".join(report_lines)

# --- Функции для измерения ---

def get_network_io_total():
    """Получает общий объем отправленных и полученных данных."""
    try:
        net_io = psutil.net_io_counters()
        return {"total_sent": net_io.bytes_sent, "total_recv": net_io.bytes_recv}
    except Exception:
        return None

def get_network_speed():
    """Измеряет скорость загрузки, выгрузки и получает данные о сервере Speedtest."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        server = st.best
        download_speed = st.download() / 10**6
        upload_speed = st.upload() / 10**6
        
        return {
            "download_speed_mbps": download_speed, "upload_speed_mbps": upload_speed,
            "server_name": server['host'], "server_location": f"{server['country']} ({server['name']})",
            "server_latency": server['latency']
        }
    except Exception:
        return None

def get_ping_and_loss(target, count=4):
    """Измеряет средний пинг и процент потери пакетов."""
    try:
        result = python_ping(target, count=count, timeout=2) 
        return {"avg_ping_ms": result.rtt_avg_ms, "packet_loss_percent": result.packet_loss}
    except Exception:
        return None

def get_local_net_details():
    """Получает локальный IP, MAC-адрес, имя активного интерфейса и IP шлюза."""
    details = {"local_ip": None, "mac_address": None, "interface_name": None, "gateway_ip": None}
    
    try:
        gws = netifaces.gateways()
        default_route = gws.get('default', {}).get(netifaces.AF_INET)
        
        if default_route:
            details['gateway_ip'] = default_route[0]
            active_interface = default_route[1]
            details['interface_name'] = active_interface

            addrs = netifaces.ifaddresses(active_interface)
            
            if netifaces.AF_INET in addrs:
                details['local_ip'] = addrs[netifaces.AF_INET][0]['addr']
                
            if netifaces.AF_LINK in addrs:
                details['mac_address'] = addrs[netifaces.AF_LINK][0]['addr'].upper().replace('-', ':')

    except Exception:
        pass 
    return details

def get_system_info():
    """Собирает имя хоста и внешний IP."""
    info = {"hostname": None, "external_ip": None}

    try:
        info["hostname"] = socket.gethostname()
    except:
        pass

    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        info["external_ip"] = response.json().get('ip')
    except:
        pass

    return info

# --- Основной запуск ---

if __name__ == "__main__":
    
    data = {}
    target_host = 'ya.ru'
    output_filename = "network_info_report.txt"

    # Сбор данных
    print("--- 1. Сбор базовой информации (IP, MAC, Hostname) ---")
    data.update(get_system_info())
    data.update(get_local_net_details()) 
    io_data = get_network_io_total()
    if io_data:
        data.update(io_data)
    print("Базовые данные собраны. ✅")

    # Пинги
    if data.get('gateway_ip'):
        print(f"\n--- 2. Проверка пинга до шлюза ({data['gateway_ip']}) ---")
        ping_gw_data = get_ping_and_loss(data['gateway_ip'])
        if ping_gw_data:
            data["ping_gateway_ms"] = ping_gw_data["avg_ping_ms"]
            data["loss_gateway_percent"] = ping_gw_data["packet_loss_percent"]
        print("Проверка завершена. 📶")

    print(f"\n--- 3. Проверка пинга до {target_host} ---")
    ping_ext_data = get_ping_and_loss(target=target_host)
    if ping_ext_data:
        data["ping_ya_ru_ms"] = ping_ext_data["avg_ping_ms"]
        data["loss_ya_ru_percent"] = ping_ext_data["packet_loss_percent"]
    print("Проверка завершена. 🎯")
    
    # Speedtest
    print("\n--- 4. Проверка скорости сети (Speedtest) ---")
    speed_data = get_network_speed()
    if speed_data:
        data.update(speed_data)
        print("Тестирование скорости завершено. 🚀")
    else:
        print("Тестирование скорости не выполнено (проверьте интернет-соединение).")

    # Форматирование и вывод отчета
    report_content = format_report(data, target_host)
    
    print(report_content)
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"\n✅ Отчет успешно сохранен в файле: {output_filename} в папке {os.getcwd()}")
    except Exception as e:
        print(f"\n❌ Ошибка при записи отчета в файл: {e}")