import os
from datetime import datetime

import openpyxl

class DataExporter:
    def __init__(self):
        self.file_name = f"match_data_{datetime.now().timestamp()}.xlsx"
        self.file_path = os.path.join("out/data", self.file_name)

        self._workbook = openpyxl.Workbook()
        self._sheet = self._workbook.active
        self._sheet.title = "Данные матчей"
        self._sheet.append([
            "Команда 1", "Команда 2", "Турнир", "url",
            "место_1", "общий_в1", "общий_н1", "общий_п1", "очки_1",
            "место_2", "общий_в2", "общий_н2", "общий_п2", "очки_2",
            "дома_место1", "дома_в1", "дома_н1", "дома_п1", "дома_о1",
            "гости_место2", "гости_в2", "гости_н2", "гости_п2", "гости_о2",
            "форма_в1", "форма_н1", "форма_п1", "форма_в2", "форма_н2", "форма_п2",
            "Имя", "Год_стат_игрок", "Амплуа", "Рейтинг", "Игр сыграно", "Голы", "Передачи",
            "Желтые карточки", "Красные карточки", "Стоимость игрока",
            "выйгрыши_с_соседями_1", "ничьи_с_соседями_1", "проигрыши_с_соседями_1",
            "выйгрыши_с_соседями_2", "ничьи_с_соседями_2", "проигрыши_с_соседями_2",
            "коэф_команда1", "коэф_ничья", "коэф_команда2",
            "Следущая игра к1", "Дата следующей игры к1",
            "Следущая игра к2", "Дата следующей игры к2", "Дата"
        ])

    def _save_workbook(self):
        self._workbook.save(self.file_path)

    def _build_main_row(self, match, player):
        return [
            match['home_team_name'],
            match['away_team_name'],
            match['tournament'],
            match['match_url'],
            match['home_team']['place'],
            match['home_team']['wins'],
            match['home_team']['draws'],
            match['home_team']['losses'],
            match['home_team']['points'],

            match['away_team']['place'],
            match['away_team']['wins'],
            match['away_team']['draws'],
            match['away_team']['losses'],
            match['away_team']['points'],

            match['standings_home']['place'],
            match['standings_home']['wins'],
            match['standings_home']['draws'],
            match['standings_home']['losses'],
            match['standings_home']['points'],

            match['standings_away']['place'],
            match['standings_away']['wins'],
            match['standings_away']['draws'],
            match['standings_away']['losses'],
            match['standings_away']['points'],

            match['home_team_form']['wins'],
            match['home_team_form']['draws'],
            match['home_team_form']['losses'],

            match['away_team_form']['wins'],
            match['away_team_form']['draws'],
            match['away_team_form']['losses'],
        ] + [
            player['name'], player['season'], player['role'], player['rating'], player['games'], player['goals'],
            player['transfers'], player['yellow_cards'], player['red_cards'], player['price']
        ] + [
            match["home_team_rivals"]["wins"],
            match["home_team_rivals"]["draws"],
            match["home_team_rivals"]["losses"],
            match["away_team_rivals"]["wins"],
            match["away_team_rivals"]["draws"],
            match["away_team_rivals"]["losses"],
            match['odds'][0],
            match['odds'][1],
            match['odds'][2],
            match["home_team_rivals"]["next_game_name"],
            match["home_team_rivals"]["next_game_date"],
            match["away_team_rivals"]["next_game_name"],
            match["away_team_rivals"]["next_game_date"],
            match['start_time']
        ]

    def _build_player_row(self, player):
        return [""] * 30 + [
            player['name'], player['season'], player['role'], player['rating'], player['games'], player['goals'],
            player['transfers'], player['yellow_cards'], player['red_cards'], player['price']
        ]

    def to_excel(self, data):
        # os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        for index, player in enumerate(data["inactive_players"]):
            if index == 0:
                # Основная строка с данными матча
                row = self._build_main_row(data, player)
            else:
                # Строки только с игроками
                row = self._build_player_row(player)

            self._sheet.append(row)
            # test[index+9] = link

        # self._sheet.append(test)

        self._save_workbook()