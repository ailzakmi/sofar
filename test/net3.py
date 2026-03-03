import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Таймауты
REQUEST_TIMEOUT = 10
MAX_WORKERS = 10  # Максимум 10 параллельных запросов


def check_client(url: str) -> Dict[str, Any]:
    """
    Проверяет один клиент: делает GET-запрос и возвращает результат.
    """
    start_time = time.time()
    result = {
        "url": url,
        "status": None,
        "response_time": None,
        "error": None,
    }

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        result["status"] = response.status_code
        result["response_time"] = round(time.time() - start_time, 3)

        if 200 <= response.status_code < 300:
            logger.info(f"￼ Успешно: {url} — {response.status_code} за {result['response_time']}s")
        else:
            logger.warning(f"￼ Неожиданный статус: {url} — {response.status_code}")

    except requests.exceptions.Timeout:
        result["error"] = "timeout"
        logger.error(f"￼ Таймаут: {url}")
    except requests.exceptions.ConnectionError:
        result["error"] = "connection_error"
        logger.error(f"￼ Ошибка соединения: {url}")
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
        logger.error(f"￼ Ошибка запроса {url}: {e}")

    return result


def request_logging(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Многопоточный опрос списка URL с ограничением числа потоков.
    Возвращает список результатов.
    """
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Отправляем все задачи
        future_to_url = {executor.submit(check_client, url): url for url in urls}

        # Собираем результаты по мере завершения
        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)

    return results


# Пример использования
if __name__ == "__main__":
    client_urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/500",
        "https://example.com",
        "https://ya.ru",
        "https://nonexistent.local",  # будет ошибка
        "https://github.com",
        "https://stackoverflow.com",
        "https://httpbin.org/delay/5",  # длинная задержка
    ] * 3  # Увеличим для демонстрации

    print(f"Запуск опроса {len(client_urls)} клиентов с макс. {MAX_WORKERS} потоками...\n")

    start = time.time()
    results = request_logging(client_urls)
    duration = time.time() - start

    print(f"\nГотово за {duration:.2f} секунд")
    print(f"Успешно: {sum(1 for r in results if r['status'] and 200 <= r['status'] < 300)}")
    print(f"Ошибки: {sum(1 for r in results if r['error'])}")