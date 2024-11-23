import time
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver

from app.parsers.base_parser import BaseParser
from logger import logger


class MatchParser(BaseParser):
    def get_tournament(self):
        element = self.find(By.CSS_SELECTOR, ".tournamentHeader__country")

        if not element:
            return "-"

        return element.text.strip().split(" - ")[0]

    def get_odds(self):
        elements = self.find_all(By.CSS_SELECTOR, ".odds .oddsValue")

        if not elements:
            return ["-" for _ in range(1, 3)]

        return [el.text.strip() for el in elements]

    def get_inactive_player_links(self):
        elements = self.find_all(By.CSS_SELECTOR, ".lf__participantNew a")

        if not elements:
            return []

        return [el.get_attribute("href").strip() for el in elements]

    def get_rivals(self):
        standings_btn = self.find(By.XPATH, "//a[contains(@href, '#/standings')]")
        if standings_btn is None:
            return []

        standings_btn.click()
        time.sleep(2)

        names = self.find_all(By.CSS_SELECTOR, ".ui-table__row .tableCellParticipant__name")

        return [name.text.strip() for name in names]

    def get_standings(self, team):
        result = {
            'place': '-',
            'wins': '-',
            'draws': '-',
            'losses': '-',
            'points': '-'
        }

        standings_btn = self.find(By.XPATH, "//a[contains(@href, '#/standings')]")

        if standings_btn is None:
            return result

        standings_btn.click()
        time.sleep(4)

        standings_btn = self.find(By.XPATH, "//a[contains(@href, '#/standings/table')]")

        if standings_btn is None:
            return result

        standings_btn.click()
        time.sleep(2)

        cols = self.find_all(By.XPATH, f"//div[contains(@class, 'ui-table__row') and .//a[text()='{team}']]//*[contains(@class, 'table__cell')]")

        if not cols:
            return result

        result['place'] = cols[0].text.strip()[:-1]
        result['wins'] = cols[3].text.strip()
        result['draws'] = cols[4].text.strip()
        result['losses'] = cols[5].text.strip()
        result['points'] = cols[8].text.strip()

        return result

    def get_standings_home(self, team):
        result = {
            'place': '-',
            'wins': '-',
            'draws': '-',
            'losses': '-',
            'points': '-'
        }

        standings_btn = self.find(By.XPATH, "//a[contains(@href, '#/standings/table/home')]")

        if standings_btn is None:
            return result

        standings_btn.click()
        time.sleep(4)

        cols = self.find_all(By.XPATH,
                             f"//div[contains(@class, 'ui-table__row') and .//a[text()='{team}']]//*[contains(@class, 'table__cell')]")

        if not cols:
            return result

        result['place'] = cols[0].text.strip()[:-1]
        result['wins'] = cols[3].text.strip()
        result['draws'] = cols[4].text.strip()
        result['losses'] = cols[5].text.strip()
        result['points'] = cols[8].text.strip()

        return result

    def get_standings_away(self, team):
        result = {
            'place': '-',
            'wins': '-',
            'draws': '-',
            'losses': '-',
            'points': '-'
        }

        standings_btn = self.find(By.XPATH, "//a[contains(@href, '#/standings/table/away')]")
        if standings_btn is None:
            return result

        standings_btn.click()
        time.sleep(4)

        cols = self.find_all(By.XPATH,
                             f"//div[contains(@class, 'ui-table__row') and .//a[text()='{team}']]//*[contains(@class, 'table__cell')]")

        if not cols:
            return result

        result['place'] = cols[0].text.strip()[:-1]
        result['wins'] = cols[3].text.strip()
        result['draws'] = cols[4].text.strip()
        result['losses'] = cols[5].text.strip()
        result['points'] = cols[8].text.strip()

        return result

    def get_standings_form(self, team):
        result = {
            'wins': '-',
            'draws': '-',
            'losses': '-',
        }

        standings_btn = self.find(By.XPATH, "//a[contains(@href, '#/standings/form')]")
        if standings_btn is None:
            return result

        standings_btn.click()
        time.sleep(4)

        cols = self.find_all(By.XPATH,
                             f"//div[contains(@class, 'ui-table__row') and .//a[text()='{team}']]//*[contains(@class, 'table__cell')]")

        if not cols:
            return result

        result['wins'] = cols[3].text.strip()
        result['draws'] = cols[4].text.strip()
        result['losses'] = cols[5].text.strip()

        return result


    def get_match_data(self):
        data = {
            "tournament": self.get_tournament(),
            "home_team_name": self.get_text(By.CSS_SELECTOR, ".duelParticipant__home"),
            "home_team_link": self.get_link(By.CSS_SELECTOR, ".duelParticipant__home a"),
            "away_team_name": self.get_text(By.CSS_SELECTOR, ".duelParticipant__away"),
            "away_team_link": self.get_link(By.CSS_SELECTOR, ".duelParticipant__away a"),
            "start_time": self.get_text(By.CSS_SELECTOR, ".duelParticipant__startTime"),
            "odds": self.get_odds(),
            "inactive_player_links": self.get_inactive_player_links(),
            "rivals": self.get_rivals()
        }

        data['home_team'] = self.get_standings(data['home_team_name'])
        data['away_team'] = self.get_standings(data['away_team_name'])
        data['standings_home'] = self.get_standings_home(data['home_team_name'])
        data['standings_away'] = self.get_standings_away(data['away_team_name'])
        data["home_team_form"] = self.get_standings_form(data['home_team_name'])
        data["away_team_form"] = self.get_standings_form(data['away_team_name'])

        # input("skhdksdkfk")

        return data

