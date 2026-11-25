"""Append one registration from a GitHub issue body to data/registrations.json."""

import json
import os
import re
import sys

PATH = os.environ.get("REGISTRATIONS_PATH", os.path.join("data", "registrations.json"))
FIELDS = ("name", "aoc", "github", "linkedin", "city", "division", "comms", "ai", "notes")
DIVISIONS = {"", "beginner", "intermediate", "advanced"}
COMMS = {"", "discord", "github", "both"}
AI = {"", "true", "false"}


def report(status: str, message: str) -> int:
    print(f"STATUS={status}")
    print(message)
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"status={status}\n")
            handle.write(f"message={message}\n")
    return 0


def clean_line(value: str, limit: int) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


def profile_url(value: str, kind: str) -> str:
    value = value.strip().split("?")[0].split("#")[0].rstrip("/")
    if not value:
        return ""
    if kind == "github":
        match = re.fullmatch(r"https://github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)", value)
        if not match:
            raise ValueError("GitHub profile must look like https://github.com/username")
        return f"https://github.com/{match.group(1)}"
    match = re.fullmatch(r"https://(?:www\.)?linkedin\.com/in/([A-Za-z0-9\-_%]+)", value, re.IGNORECASE)
    if not match:
        raise ValueError("LinkedIn profile must look like https://www.linkedin.com/in/username")
    return f"https://www.linkedin.com/in/{match.group(1)}"


def parse_body(body: str) -> dict:
    match = re.search(r"```registration\s*(.*?)```", body, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError("Registration block is missing")
    found = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        found[key.strip().lower()] = value.strip()
    entry = {
        "name": clean_line(found.get("name", ""), 80),
        "aoc": clean_line(found.get("aoc", ""), 80),
        "github": profile_url(found.get("github", ""), "github"),
        "linkedin": profile_url(found.get("linkedin", ""), "linkedin"),
        "city": clean_line(found.get("city", ""), 80),
        "division": found.get("division", "").strip().lower(),
        "comms": found.get("comms", "").strip().lower(),
        "ai": found.get("ai", "").strip().lower(),
        "notes": clean_line(found.get("notes", ""), 500),
    }
    if not entry["name"] or not entry["aoc"]:
        raise ValueError("Name and Advent of Code username are required")
    if not entry["github"] and not entry["linkedin"]:
        raise ValueError("Add a GitHub or LinkedIn profile")
    if entry["division"] not in DIVISIONS or entry["comms"] not in COMMS or entry["ai"] not in AI:
        raise ValueError("Division, communication, or AI answer is not recognized")
    return entry


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    try:
        entry = parse_body(body)
    except ValueError as error:
        return report("INVALID", str(error))

    with open(PATH, "r", encoding="utf-8") as handle:
        people = json.load(handle)
    if any(person.get("aoc", "").strip().lower() == entry["aoc"].lower() for person in people):
        return report("DUPLICATE", f"{entry['aoc']} is already registered")

    people.append(entry)
    people.sort(key=lambda person: person.get("name", "").lower())
    with open(PATH, "w", encoding="utf-8") as handle:
        json.dump(people, handle, indent=2)
        handle.write("\n")
    return report("ADDED", f"Registered {entry['name']}")


if __name__ == "__main__":
    sys.exit(main())
