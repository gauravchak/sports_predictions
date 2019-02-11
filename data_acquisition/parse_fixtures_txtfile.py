'''
Parse the fixtures file and write the names of the teams in 1-premierleague-teams.csv
'''
import argparse
import re
from typing import Set


def get_game_fixture_text(t_line: str) -> str:
    '''Returns just the matched part. If no part matched returns empty string'''
    # Text like: Fulham 09:45 Liverpool   Craven Cottage, London
    one_one = re.compile(r'[a-zA-Z]+\s+\d+:\d+\s[a-zA-Z]+\s\s+')
    # Text like: Fulham 09:45 Man Utd   Craven Cottage, London
    one_two = re.compile(r'[a-zA-Z]+\s+\d+:\d+\s[a-zA-Z]+\s[a-zA-Z]+\s\s+')
    # Text like: West Ham 10:00 Fulham   somewhere, sdfsd
    two_one = re.compile(r'[a-zA-Z]+\s[a-zA-Z]+\s+\d+:\d+\s[a-zA-Z]+\s\s+')
    # Text like: West Ham 10:00 Man Utd   somewhere, sdfsd
    two_two = re.compile(r'[a-zA-Z]+\s[a-zA-Z]+\s+\d+:\d+\s[a-zA-Z]+\s[a-zA-Z]+\s\s+')

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


def process_fixtures_file(fixturesfile: str) -> Set[str]:
    '''Parse the fixtures txtfile and return a list of strings, each of which is a team name.

    Contents are like:
    Date To Be Confirmed
    Chelsea TBC Brighton   Stamford Bridge, London  
    Quick View
    Monday 11 February 2019
    Wolves TBC Newcastle   Molineux Stadium, Wolverhampton  Live On Live stream available for this match.
    Friday 22 February 2019
    Cardiff 14:45 Watford   Cardiff City Stadium, Cardiff  
    '''
    set_of_teams = set([])
    with open(fixturesfile) as txtf_hndl:
        list_of_lines = txtf_hndl.readlines()
    # Remove whitespace characters like `\n` at the end of each line
    list_of_lines = [x.strip() for x in list_of_lines]
    for t_line in list_of_lines:
        # ignore empty line
        if not t_line:
            continue
        # ignore line with all spaces
        if t_line.isspace():
            continue
        # split into words to see length
        t_words = t_line.split()
        if (len(t_words) >= 4):
            # valid game fixtures lines should have at least four words team time team venue
            game_fixture = get_game_fixture_text(t_line)
            # Now try to do regex matching and extract the team names
            c_dict = re.match(r"(?P<home_team>[\D]+)\s(?P<hh>\d+):(?P<mm>\d+)\s(?P<away_team>[\D]+)", game_fixture)
            if c_dict:
                home_team = c_dict['home_team'].lstrip()
                away_team = c_dict['away_team'].rstrip()
                set_of_teams.add(home_team)
                set_of_teams.add(away_team)
    return set_of_teams


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fixturesfile", help="The txt file got by cutpaste from https://www.premierleague.com/results")
    parser.add_argument("teamsfile", help="The file to write team names in")
    args = parser.parse_args()
    teamnames = process_fixtures_file(args.fixturesfile)
    if teamnames:
        # if the liste returned is valid then write it to file
        with open(args.teamsfile, 'w') as tfhndl:
            for item in teamnames:
                tfhndl.write("{}\n".format(item))
