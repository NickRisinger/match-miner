import time
from selenium.webdriver.common.by import By

from app.parsers.base_parser import BaseParser
from logger import logger


class PlayerParser(BaseParser):
    def get_inactive_players(self, links: list[str]):
        players = []

        if links:
            for link in links:
                logger.info(f"Парсинг игрока: {link}")
                self.driver.get(link)
                time.sleep(4)

                player = {
                    "name": self.get_text(By.CSS_SELECTOR, ".playerHeader__nameWrapper h2"),
                    "role": self.get_text(By.CSS_SELECTOR, ".playerTeam strong"),
                    "price": self.get_text(By.XPATH, "//div[contains(@class, 'playerInfoItem') and .//strong[text()='Рыночная цена']]//span"),
                    "season": "-",
                    "rating": "-",
                    "games": "-",
                    "goals": "-",
                    "transfers": "-",
                    "yellow_cards": "-",
                    "red_cards": "-",
                }

                row = self.find(By.CSS_SELECTOR, "#league-table .careerTab__row:not(.careerTab__row--main)")
                if row is not None:
                    player["season"] = row.find_element(By.CSS_SELECTOR, ".careerTab__season").text.strip()
                    stats = row.find_elements(By.CSS_SELECTOR, ".careerTab__stat")
                    player["rating"] = stats[0].text.strip()
                    player["games"] = stats[1].text.strip()
                    player["goals"] = stats[2].text.strip()
                    player["transfers"] = stats[3].text.strip()
                    player["yellow_cards"] = stats[4].text.strip()
                    player["red_cards"] = stats[5].text.strip()

                players.append(player)

        else:
            players.append({
                    "name": "-",
                    "role": "-",
                    "price": "-",
                    "season": "-",
                    "rating": "-",
                    "games": "-",
                    "goals": "-",
                    "transfers": "-",
                    "yellow_cards": "-",
                    "red_cards": "-",
                })

        return players