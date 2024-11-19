import logging
import os
from datetime import datetime

from config import LOG_FILE

os.makedirs("out/data", exist_ok=True)
os.makedirs(LOG_FILE, exist_ok=True)

# Создаем логгер
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Обработчик для файла
file_handler = logging.FileHandler(f'{LOG_FILE}/app_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Пример логов
# logger.debug("Отладочное сообщение.")
# logger.info("Информация.")
# logger.warning("Предупреждение.")
# logger.error("Ошибка.")
# logger.critical("Критическая ошибка.")