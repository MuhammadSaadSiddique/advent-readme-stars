from dataclasses import dataclass
from typing import Generator

import requests

from advent_readme_stars.constants import SESSION_COOKIE,  USER_ID, YEAR


@dataclass(frozen=True, eq=True)
class DayProgress:
    day: int
    part_1: bool
    part_2: bool


def get_progress() -> Generator[DayProgress, None, None]:
    for y in YEAR.split(","):
        STARS_ENDPOINT = f"{ADVENT_URL}/{y}/leaderboard/private/view/{LEADERBOARD_ID}.json"
        res = requests.get(STARS_ENDPOINT, cookies={"session": SESSION_COOKIE})
        res.raise_for_status()
    
        leaderboard_info = res.json()
        
        file = open(f"{y}.py", 'w')
        file.write(leaderboard_info)
        file.close()
        for member,detail in leaderboard_info["members"].items():
            stars = member["completion_day_level"]
        
            for day, parts in stars.items():
                completed = parts.keys()
                yield DayProgress(
                    member["name"],
                    member["local_score"]
                    day=int(day),
                    part_1="1" in completed,
                    part_2="2" in completed,
                )
