import psutil
import time
from tabulate import tabulate

def get_cpu_usage():

    return psutil.cpu_percent(interval=1)

def get_memory_usage():
 
    memory = psutil.virtual_memory()
    return {
        'Всего': f'{memory.total / (1024**3):.2f} ГБ',
        'Используется': f'{memory.used / (1024**3):.2f} ГБ',
        'Свободно': f'{memory.available / (1024**3):.2f} ГБ',
        'Процент использования': f'{memory.percent}%'
    }

def get_top_processes(n=10):

    processes = []
    for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), 
                       key=lambda x: x.info['cpu_percent'], 
                       reverse=True)[:n]:
        try:
            processes.append([
                proc.info['pid'], 
                proc.info['name'], 
                f"{proc.info['cpu_percent']:.2f}%", 
                f"{proc.info['memory_percent']:.2f}%"
            ])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes

def main():

    print("=== Мониторинг системы ===")
    

    print(f"\nЗагрузка CPU: {get_cpu_usage()}%")
    

    print("\nИспользование памяти:")
    for key, value in get_memory_usage().items():
        print(f"{key}: {value}")
    

    print("\nТоп процессов по использованию CPU:")
    top_processes = get_top_processes()
    print(tabulate(top_processes, 
                   headers=['PID', 'Название', 'CPU %', 'Память %'], 
                   tablefmt='grid'))

if __name__ == '__main__':
    main()
