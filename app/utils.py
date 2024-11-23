import re


JS_ROW_END = '~'
JS_CELL_END = '¬'
JS_INDEX = '÷'


def is_valid_url(url):
    pattern = r'^https://www\.flashscorekz\.com/match/[a-zA-Z0-9]+/#/match-summary$'
    return re.match(pattern, url) is not None

def transform_standings(data: str):
    rows = data.split(JS_ROW_END)
    rows_length = len(rows)
    result = []

    for i in range(rows_length):
        tmp = {}
        row = rows[i].split(JS_CELL_END)
        row_length = len(row) - 1
        index = row[0].split(JS_INDEX)

        index_name = None
        index_value = None

        if len(index) > 0:
            index_name = index[0]
        if len(index) > 1:
            index_value = index[1]

        if index_name == '':
            continue

        for j in range(row_length):
            rowParts = row[j].split(JS_INDEX)

            if len(rowParts) == 2:
                tmp[rowParts[0]] = rowParts[1]

        result.append(tmp)

    return result


def extract_teams(table: list[str], start, end: int) -> list[str]:
    return [table[i] for i in range(start, end + 1) if 0 <= i < len(table)]


def get_rival_team(name: str, table: list[str]):
    team_index = -1

    # Поиск индекса команды
    for i, row in enumerate(table):
        if row == name:
            team_index = i
            break

    if team_index == -1:
        return []

    if team_index < 4:  # 1-е место
        rivals = extract_teams(table, 0, 4)
    elif team_index > len(table) - 4:  # Последнее место
        rivals = extract_teams(table, len(table) - 5, len(table))
    else:  # Все остальные случаи
        rivals = extract_teams(table, team_index - 3, team_index + 3)

    return rivals