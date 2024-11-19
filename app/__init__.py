from app.exporter import DataExporter
from app.scraper.flashscore_scraper import FlashscoreScraper
from logger import logger


def run(links: list[str]) -> None:
    scraper = FlashscoreScraper()
    data_exporter = DataExporter()

    try:
        for link in links:
            logger.info(f"Парсинг матча: {link}")
            data = scraper.parse_match(link)
            logger.info(data)
            data_exporter.to_excel(data)
            logger.info("Данные успешно сохранены")
        # raise Exception('Тестирование ошибок')
    except Exception as e:
        logger.error(e, stack_info=True)
    finally:
        scraper.close()
