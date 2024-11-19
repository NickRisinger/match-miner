import time

from app.parsers.match_parser import MatchParser
from app.parsers.player_parser import PlayerParser
from app.parsers.team_parser import TeamParser
from app.scraper.base_scraper import BaseScraper
from app.utils import get_rival_team
from logger import logger


class FlashscoreScraper(BaseScraper):
    def parse_match(self, match_url):
        self.driver.get(match_url)
        time.sleep(4)

        match_parser = MatchParser(self.driver)
        data = match_parser.get_match_data()
        data['match_url'] = match_url

        team_parser = TeamParser(self.driver)
        logger.debug(f"home_team_rivals: {get_rival_team(data['away_team_name'], data['rivals'])}")
        data['home_team_rivals'] = team_parser.get_team_data(data['home_team_link'],
                                                            get_rival_team(data['away_team_name'],
                                                                           data['rivals']))
        logger.debug(f"away_team_rivals: {get_rival_team(data['home_team_name'], data['rivals'])}")
        data['away_team_rivals'] = team_parser.get_team_data(data['away_team_link'],
                                                            get_rival_team(data['home_team_name'],
                                                                           data['rivals']))

        player_parser = PlayerParser(self.driver)
        data['inactive_players'] = player_parser.get_inactive_players(data['inactive_player_links'])
        print(data['inactive_players'])

        return data
