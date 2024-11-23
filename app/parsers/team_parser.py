import time
import requests
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver

from app.parsers.base_parser import BaseParser
from app.utils import transform_standings
from logger import logger


class TeamParser(BaseParser):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.participant = None
        self.country = None


    def get_team_data(self, url: str, rivals: list[str]):
        self.auth()

        logger.info(f"Парсинг команды: {url}")
        self.driver.get(url)
        time.sleep(4)

        self.participant = self.driver.execute_script("return window.participant;")
        self.country = self.driver.execute_script("return window.country_id;")

        result = {
            'name': self.get_text(By.CSS_SELECTOR, ".heading__name"),
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'next_game_name': '-',
            'next_game_date': '-',
        }

        filtered = list(filter(lambda r: r != result['name'], rivals))
        page = 0
        games = []
        current_date_minus_one_year = int((datetime.now() - timedelta(days=365)).timestamp())

        logger.debug(f"Соперники: {filtered}")
        print(f'send: https://46.flashscore.ninja/46/x/feed/pr_1_{self.country}_{self.participant}_{page}_3_ru-kz_1')

        while True:
            resp = requests.get(
                f'https://46.flashscore.ninja/46/x/feed/pr_1_{self.country}_{self.participant}_{page}_3_ru-kz_1',
                headers={
                    "x-fsign": self.api_key,
                })

            data = [item for item in transform_standings(resp.text) if 'AA' in item]

            print(data)

            date = int(data[len(data) - 1]['AD'])

            games += data

            if date - current_date_minus_one_year > 0:
                page += 1
                continue
            else:
                print('Все гуд это последний матч!', datetime.fromtimestamp(int(date)))
                break

        for game in games:
            print("Game:", game)
            if int(game['AD']) - current_date_minus_one_year > 0:
                if game['PY'] == self.participant and game['AE'] in filtered:
                    if game['AH'] == game['AG']:
                        result['draws'] += 1
                    if game['AH'] > game['AG']:
                        result['wins'] += 1
                    if game['AH'] < game['AG']:
                        result['losses'] += 1

                if game['PX'] == self.participant and game['AF'] in filtered:
                    if game['AG'] == game['AH']:
                        result['draws'] += 1
                    if game['AG'] > game['AH']:
                        result['wins'] += 1
                    if game['AG'] < game['AH']:
                        result['losses'] += 1


        logger.debug(f"{result}")
        time.sleep(2)


        fixtures_btn = self.find(By.CSS_SELECTOR, "a.fixtures")
        if fixtures_btn is None:
            return result

        print("finds btn")

        fixtures_btn.click()
        time.sleep(4)

        row = self.find(By.XPATH, "//div[@data-event-row='true'][2]")

        if row is None:
            return result

        print("finds row", row)

        home_team = row.find_element(By.CSS_SELECTOR, ".event__homeParticipant").text.strip()
        away_team = row.find_element(By.CSS_SELECTOR, ".event__awayParticipant").text.strip()

        result['next_game_date'] = row.find_element(By.CSS_SELECTOR, ".event__time").text.strip()

        if home_team == result["name"]:
            result['next_game_name'] = away_team

        if away_team == result["name"]:
            result['next_game_name'] = home_team

        return result