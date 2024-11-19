import time

from selenium.webdriver.common.by import By

from app.parsers.base_parser import BaseParser
from logger import logger


class TeamParser(BaseParser):
    def get_team_data(self, url: str, rivals: list[str]):
        logger.info(f"Парсинг команды: {url}")
        self.driver.get(url)
        time.sleep(4)

        result = {
            'name': self.get_text(By.CSS_SELECTOR, ".heading__name"),
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'next_game_name': '-',
            'next_game_date': '-',
        }

        results_btn = self.find(By.CSS_SELECTOR, "a.results")
        if not results_btn:
            return result

        results_btn.click()
        time.sleep(4)

        filtered = list(filter(lambda r: r != result['name'], rivals))
        logger.debug(f"Соперники: {filtered}")

        rows = self.find_all(By.CSS_SELECTOR, "div[data-event-row='true']")
        for row in rows:
            event_time = row.find_element(By.CSS_SELECTOR, ".event__time").text.strip()
            home_team = row.find_element(By.CSS_SELECTOR,
                                         ".event__homeParticipant [data-testid='wcl-scores-simpleText1']").text.strip()
            away_team = row.find_element(By.CSS_SELECTOR,
                                         ".event__awayParticipant [data-testid='wcl-scores-simpleText1']").text.strip()
            result_button = row.find_element(By.CSS_SELECTOR, "button").text.strip()

            # logger.debug(f"Данные: {event_time} - {home_team} - {away_team} - {result_button}")


            if len(event_time.split(" ")) != 2:
                continue

            if home_team not in filtered and away_team not in filtered:
                continue

            if result_button == "В":
                result['wins'] = result['wins'] + 1

            if result_button == "Н":
                result['draws'] = result['draws'] + 1

            if result_button == "П":
                result['losses'] = result['losses'] + 1

        fixtures_btn = self.find(By.CSS_SELECTOR, "a.fixtures")
        if not results_btn:
            return result

        fixtures_btn.click()
        time.sleep(4)

        row = self.find(By.XPATH, "//div[@data-event-row='true'][2]")

        if row is None:
            return result

        home_team = row.find_element(By.CSS_SELECTOR, ".event__homeParticipant").text.strip()
        away_team = row.find_element(By.CSS_SELECTOR, ".event__awayParticipant").text.strip()

        result['next_game_date'] = row.find_element(By.CSS_SELECTOR, ".event__time").text.strip()

        if home_team == result["name"]:
            result['next_game_name'] = away_team

        if away_team == result["name"]:
            result['next_game_name'] = home_team

        return result