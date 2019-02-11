'''
This file is used for data acquisition.
For example, eng-england/2010s/2018-19/1-premierleague.txt txt file was created by copy paste from 
https://www.premierleague.com/results
Run `python process_premier_league_results_page.py 1-premierleague.txt` in the directory eng-england/2010s/2018-19
It will produce `1-premierleague-sep.csv`

TODO: This can be improved by looking at fixtures file and parsing team names.
'''
import argparse
import re
from datetime import date, datetime

import pandas as pd


def get_game_text(t_line: str) -> str:
    '''Returns just the matched part. If no part matched returns empty string'''
    # Text like: Fulham 0-3 Liverpool   Craven Cottage, London
    one_one = re.compile(r'[a-zA-Z]+\s+\d+-\d+\s[a-zA-Z]+\s\s+')
    # Text like: Fulham 0-3 Man Utd   Craven Cottage, London
    one_two = re.compile(r'[a-zA-Z]+\s+\d+-\d+\s[a-zA-Z]+\s[a-zA-Z]+\s\s+')
    # Text like: West Ham 0-3 Fulham   somewhere, sdfsd
    two_one = re.compile(r'[a-zA-Z]+\s[a-zA-Z]+\s+\d+-\d+\s[a-zA-Z]+\s\s+')
    # Text like: West Ham 0-3 Man Utd   somewhere, sdfsd
    two_two = re.compile(r'[a-zA-Z]+\s[a-zA-Z]+\s+\d+-\d+\s[a-zA-Z]+\s[a-zA-Z]+\s\s+')

    game_text = ''
    m11 = one_one.match(t_line)
    if m11 is not None:
        game_text = m11.group()
    m12 = one_two.match(t_line)
    if m12 is not None:
        game_text = m12.group()
    m21 = two_one.match(t_line)
    if m21 is not None:
        game_text = m21.group()
    m22 = two_two.match(t_line)
    if m22 is not None:
        game_text = m22.group()
    return game_text


def process_file(txtfilename: str) -> pd.DataFrame:
    '''Returns a dataframe with columns: [game_date,home_team,away_team,score_home,score_away]

    Lines are like:
    Saturday 9 February 2019 # Date change

    # space or empty line
    Fulham 0-3 Man Utd   Craven Cottage, London # game lines
    '''
    ret_df = pd.DataFrame(columns=['game_date', 'home_team', 'away_team', 'score_home', 'score_away'])

    with open(txtfilename) as txtf_hndl:
        list_of_lines = txtf_hndl.readlines()
    # Remove whitespace characters like `\n` at the end of each line
    list_of_lines = [x.strip() for x in list_of_lines]
    game_date = date.today()
    for t_line in list_of_lines:
        # ignore empty line
        if not t_line:
            continue
        # ignore line with all spaces
        if t_line.isspace():
            continue
        # split into words to see length
        t_words = t_line.split()
        if (len(t_words) == 4) and (t_words[3] == '2019' or t_words[3] == '2018'):
            # For date lines use: datetime.strptime('Saturday 9 February 2019', '%A %d %B %Y')
            game_date = datetime.strptime(t_line, '%A %d %B %Y')
        elif len(t_words) >= 3:
            game_text = get_game_text(t_line)
            if game_text:
                str1, str2 = game_text.split('-')
                home_m = re.match(r"(?P<home_team>[\D]+)\s(?P<score_home>\d+)", str1)
                home_team = home_m['home_team'].lstrip()
                score_home = home_m['score_home']
                away_m = re.match(r"(?P<score_away>\d+)\s(?P<away_team>[\D]+)", str2)
                away_team = away_m['away_team'].rstrip()
                score_away = away_m['score_away']
                ret_df.loc[len(ret_df)] = [game_date, home_team, away_team, score_home, score_away]
            else:
                print('Unhandled str = {} length = {}'.format(t_line, len(t_line)))
    ret_df = ret_df.set_index('game_date')
    return ret_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("txtfile", help="The txt file got by cutpaste from https://www.premierleague.com/results")
    args = parser.parse_args()
    results_df = process_file(args.txtfile)
    results_df.to_csv('1-premierleague-sep.csv')
