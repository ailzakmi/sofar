import psutil
import platform
import os

print("--- Общая информация о системе ---")
print(f"Операционная система: {platform.system()} {platform.release()}")
print(f"Платформа операционной системы: {platform.platform()}")
print(f"Версия операционной системы: {platform.version()}")
print(f"Архитектура: {platform.machine()}")
print(f"Имя хоста: {platform.node()}")
print(f"Пользователь: {os.getlogin()}")
print(f"Пользователь: {psutil.users()}")

print("\n--- Информация о процессоре (CPU) ---")
print(f"Количество ядер (физических/логических): {psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}")
print(f"Загрузка CPU (общая): {psutil.cpu_percent(interval=1)}%") # Загрузка за 1 секунду

print("\n--- Информация об оперативной памяти (RAM) ---")
mem = psutil.virtual_memory()
print(f"Всего памяти: {mem.total / (1024**3):.2f} GB")
print(f"Доступно: {mem.available / (1024**3):.2f} GB")
print(f"Использовано: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")

print("\n--- Информация о дисках ---")
for disk in psutil.disk_partitions():
    print(f"Диск: {disk.device}")
    try:
        usage = psutil.disk_usage(disk.mountpoint)
        print(f"  Точка монтирования: {disk.mountpoint}")
        print(f"  Всего: {usage.total / (1024**3):.2f} GB, Использовано: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
    except PermissionError:
        print("  Нет доступа к статистике диска.")

print("\n--- Информация о сети ---")
print(f"MAC-адреса: {psutil.net_if_addrs()}")