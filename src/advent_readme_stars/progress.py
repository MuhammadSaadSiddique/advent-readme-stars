from dataclasses import dataclass
from typing import Generator
import json
import requests

from advent_readme_stars.constants import SESSION_COOKIE,  USER_ID, YEAR, ADVENT_URL,LEADERBOARD_ID


@dataclass(frozen=True, eq=True)
class DayProgress:
    name: str
    score: int
    day:int
    part_1:bool
    part_1ts:int
    part_2:bool
    part_2ts:int


def get_progress(y) -> Generator[DayProgress, None, None]:
    if os.path.exists(f"{y}.json"):
        with open(f"{y}.json", 'r') as f:
            leaderboard_info=json.load(f)
    else:
        STARS_ENDPOINT = f"{ADVENT_URL}/{y}/leaderboard/private/view/{LEADERBOARD_ID}.json"
        res = requests.get(STARS_ENDPOINT, cookies={"session": SESSION_COOKIE})
        res.raise_for_status()
    
        leaderboard_info = res.json()
    
        with open(f"{y}.json", 'w') as f:
            json.dump(leaderboard_info, f)
    # members={}
    for member,detail in leaderboard_info["members"].items():
        # print(member,detail)
        
        stars = detail["completion_day_level"]
        
        for day, parts in stars.items():
            completed = parts.keys()
            
            dp= DayProgress(
                name=detail["name"],
                score=detail["local_score"],
                day=int(day),
                part_1="1" in completed,
                part_1ts=parts["1"]["get_star_ts"] if "1" in completed else -1 ,
                part_2="2" in completed,
                part_2ts=parts["2"]["get_star_ts"] if "2" in completed else -1,
            )
            # members[member]=dp
            # print(dp)
            yield dp
