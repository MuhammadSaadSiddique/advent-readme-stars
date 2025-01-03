import os

from advent_readme_stars.advent import most_recent_advent_year,most_recent_advent_year_list 

#: Advent of Code user ID
USER_ID = os.environ.get("INPUT_USERID", "")

#: Advent of Code session cookie
SESSION_COOKIE = os.environ.get("INPUT_SESSIONCOOKIE", "")

#: Advent of Code private leaderboard ID
LEADERBOARD_ID = os.environ.get("INPUT_LEADERBOARDID", "") or USER_ID

#: Marker in the README to find
TABLE_MARKER = os.environ.get("INPUT_TABLEMARKER", "<!--- advent_readme_stars table --->")

#: Star symbol to insert in the table
STAR_SYMBOL = os.environ.get("INPUT_STARSYMBOL", "<!--- advent_readme_stars table --->")

#: Years to query for
YEAR = os.environ.get("INPUT_YEAR") or most_recent_advent_year_list()

#: Year to query for
YEARS = int(os.environ.get("INPUT_YEARS")  or most_recent_advent_year())

#: Table header prefix
HEADER_PREFIX = os.environ.get("INPUT_HEADERPREFIX", "")

#: Location of the README file
README_LOCATION = os.environ.get("INPUT_READMELOCATION", "")

#: Advent of Code base URL, for testing
ADVENT_URL = os.environ.get("ADVENT_URL", "https://adventofcode.com")

#: Stars info endpoint
STARS_ENDPOINT = f"{ADVENT_URL}/{YEARS}/leaderboard/private/view/{LEADERBOARD_ID}.json"
