from typing import List

from advent_readme_stars.constants import (
    ADVENT_URL,
    HEADER_PREFIX,
    STAR_SYMBOL,
    TABLE_MARKER,
    YEAR
)
from advent_readme_stars.progress import get_progress


def remove_existing_table(lines: List[str]) -> List[str]:
    """
    If there's an existing table, it should be between two table markers.
    If that's the case, remove the existing table and return a single table
    marker in its place. If not, just return the original content.
    """
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and line.strip() == TABLE_MARKER:
            start = i
            continue
        if start is not None and line.strip() == TABLE_MARKER:
            end = i
            break

    if start is not None and end is not None:
        return lines[:start] + lines[end:]
    return lines


def insert_table(lines: List[str]) -> List[str]:
    """
    Search the lines for a table marker, and insert a table there.
    """
    table_location = None
    for i, line in enumerate(lines):
        if line.strip() == TABLE_MARKER:
            table_location = i
            break
    else:
        return lines
    to_insert=[]
    for y in YEAR.split(','):
        toinsert = [
            TABLE_MARKER,
            f"{HEADER_PREFIX} {y} Results",
            "",
            "| Name  | Score | Day | Part 1  | Part 2 |",
            "| :---:  | :---: |:---:| :---: | :---: |",
        ]
        stars_info = sorted(list(get_progress(y)), key=lambda p: p.score)
        
        for star_info in stars_info:
            name=star_info.name
            score=star_info.score
            day_url = f"{ADVENT_URL}/{y}/day/{star_info.day}"
            day_text = f"[Day {star_info.day} {y}]({day_url})"
            part_1_text = STAR_SYMBOL+ str(star_info.part_1ts) if star_info.part_1 else " "
            part_2_text = STAR_SYMBOL+ str(star_info.part_2ts) if star_info.part_2 else " "
            toinsert.append(f"| {name} | {score} | {day_text} | {part_1_text} | {part_2_text} |")
        to_insert.append(toinsert)
    return lines[:table_location] + to_insert + lines[table_location:]


def update_readme(readme: List[str]) -> List[str]:
    """
    Take the contents of a readme file and update them
    """
    reduced = remove_existing_table(readme)
    new_readme = insert_table(reduced)

    return new_readme
