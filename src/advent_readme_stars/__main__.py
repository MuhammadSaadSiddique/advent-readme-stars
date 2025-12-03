from typing import List
import datetime
import time
import json
import requests
import os
from advent_readme_stars.constants import README_LOCATION, SESSION_COOKIE, YEAR, ADVENT_URL, TABLE_MARKER
# Removed import for LEADERBOARD_ID since we are now defining multiple IDs

# --- CONFIGURATION FOR MULTIPLE LEADERBOARDS ---
# IMPORTANT: Replace these placeholder IDs with your actual AoC private leaderboard IDs
LEADERBOARDS = [
    {"id": 1739374, "name": "Team Default (Pakistan)"}, # Assuming this is your original ID
    {"id": 5206594, "name": "Team 2025"}, # Replace with your second ID
]
# YEAR="2023,2022,2021"

def timeconvert(membertime: int, day: int, year: str) -> str:
    """
    Calculates the time difference between star completion and the puzzle release time.
    AoC puzzles release at 00:00 EST, which is 05:00 UTC (or 06:00 UTC depending on DST).
    This function uses 05:00 UTC as the base puzzle start time.
    """
    # Puzzle start time (Dec 'day', 5:00:00 UTC)
    d = datetime.datetime(int(year), 12, int(day), 5, 0, 0, 0, datetime.timezone.utc)
    unix_start = int(time.mktime(d.timetuple()))

    starttime = datetime.datetime.fromtimestamp(unix_start, datetime.timezone.utc)
    completeTime = datetime.datetime.fromtimestamp(membertime, datetime.timezone.utc)

    # Return time difference formatted as string (e.g., '0:01:30')
    return str(completeTime - starttime)

def get_progress(year: str, leaderboard_id: int) -> dict:
    """Fetches and processes leaderboard data for a specific year and leaderboard ID."""
    STARS_ENDPOINT = f"{ADVENT_URL}/{year}/leaderboard/private/view/{leaderboard_id}.json"
    print(f"Fetching data for Year {year}, Leaderboard ID {leaderboard_id}...")

    try:
        res = requests.get(STARS_ENDPOINT, cookies={"session": SESSION_COOKIE}, timeout=10)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {year} (ID: {leaderboard_id}): {e}")
        return {}

    leaderboard_info = res.json()
    members = {}

    # Sort members by local_score in descending order
    sorted_members = sorted(leaderboard_info["members"].items(), 
                            key=lambda item: item[1]['local_score'], reverse=True)

    for member_id, detail in sorted_members:
        name = detail.get("name", f"Anon User {member_id}")
        score = detail["local_score"]
        stars = detail["completion_day_level"]

        if score > 0:
            # Start of the HTML row
            ft = f"<tr><th> {name} </th><th> {score} </th>"

            for d in range(1, 26):
                parts = stars.get(str(d), {})
                completed = parts.keys()
                
                # Column for Day 'd'
                ft += "<td class='long'>"
                
                # Part 1 (Silver Star)
                # If part 1 exists, show star and time; otherwise, 6 spaces for alignment
                ft += (f"⭐{timeconvert(parts['1']['get_star_ts'], d, year)}" if "1" in completed else "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
                
                # Part 2 (Gold Star)
                # If part 2 exists, show star and time; otherwise, 6 spaces for alignment
                ft += (f"⭐{timeconvert(parts['2']['get_star_ts'], d, year)}" if "2" in completed else "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
                
                ft += "</td>"
            
            ft += "</tr>"
            
            # Store the formatted row for later insertion
            members[member_id] = [name, score, ft]

    return members

def insert_table(lines: List[str]) -> List[str]:
    """
    Inserts the HTML table(s) into the list of lines at the TABLE_MARKER.
    Returns a flat list of lines.
    """
    table_location = None
    for i, line in enumerate(lines):
        if line.strip() == TABLE_MARKER:
            table_location = i
            break
    else:
        return lines

    to_insert = [TABLE_MARKER] # Keep the opening marker

    for leaderboard in LEADERBOARDS:
        leaderboard_id = leaderboard["id"]
        leaderboard_name = leaderboard["name"]
        
        for y in YEAR.split(','):
            # Header for Year and Leaderboard
            to_insert.append(f"<h2 class='text-2xl font-bold mt-8'>{leaderboard_name} - {y} Results</h2>")
            
            # Start of the table structure
            firstLine = "<div class='divTableWrapper'><div class='divTableContainer'><table class='divTable'>"
            firstLine += "<thead><tr><th> Name </th><th> Score </th>"
            
            # Day Headers
            for day in range(1, 26):
                day_url = f"{ADVENT_URL}/{y}/day/{day}"
                # Each day column will contain the two parts
                firstLine += f"<th class='long'><a href=\"{day_url}\" target='_blank' class='day-link'>Day {day}</a></th>"

            firstLine += "</tr></thead><tbody>"
            to_insert.append(firstLine)

            # Get and insert member data
            member_data = get_progress(y, leaderboard_id)
            data_sorted = {key: val for key, val in sorted(member_data.items(), 
                                                           key=lambda ele: ele[1][1], 
                                                           reverse=True)}

            for key, val in data_sorted.items():
                to_insert.append(val[2]) # val[2] is the pre-formatted <tr>...</tr> string

            # End of table structure
            to_insert.append("</tbody></table></div></div>")

    # The list now contains the original content up to the marker, the new tables, and the rest of the original content
    return lines[:table_location + 1] + to_insert[1:] + lines[table_location + 1:]

def remove_existing_table(lines: List[str]) -> List[str]:
    """
    Removes existing table content between two TABLE_MARKERs.
    """
    start = None
    end = None
    
    # Find the start and end markers
    for i, line in enumerate(lines):
        if start is None and line.strip() == TABLE_MARKER:
            start = i
            continue
        if start is not None and line.strip() == TABLE_MARKER:
            end = i
            break
            
    # If both markers are found, remove the content between them
    if start is not None and end is not None:
        # Keep the two markers, remove everything in between
        return lines[:start] + [lines[start]] + [lines[end]] + lines[end+1:]
        
    return lines

def update_readme(readme: List[str]) -> List[str]:
    """
    Take the contents of a readme file and update them
    """
    # 1. Remove any old table content (keeping the markers)
    reduced = remove_existing_table(readme)
    
    # 2. Insert the new table content
    new_readme = insert_table(reduced)
    
    return new_readme

if __name__ == "__main__":
    # The constants are imported from advent_readme_stars.constants (must be defined in your environment)
    # The SESSION_COOKIE must be set in your environment or constants file for this to work.
    
    # Check if we are ready to run
    if not SESSION_COOKIE:
        print("Error: SESSION_COOKIE is not set. Cannot fetch private leaderboard data.")
        exit(1)

    # Read the existing file
    try:
        with open(README_LOCATION, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: README file not found at {README_LOCATION}. Creating a minimal one.")
        lines = ["# Advent of Code Leaderboard", TABLE_MARKER, TABLE_MARKER]

    # Generate the updated content
    edited = update_readme(lines)

    # Write the updated content back to the file
    try:
        with open(README_LOCATION, "w", encoding="utf-8") as f:
            for line in edited:
                # Ensure each element is written as a line
                if isinstance(line, str):
                    f.write(line + "\n")
                else:
                    # Should not happen with the refactored insert_table, but for safety
                    f.write(str(line) + "\n")
        print(f"\nSuccessfully updated leaderboard tables in {README_LOCATION}.")
    except Exception as e:
        print(f"Error writing to file {README_LOCATION}: {e}")
