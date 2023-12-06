if __name__ == "__main__":
    import json
    import requests
    import datetime
    import time
    from typing import List 
    # README_LOCATION="readme.md"
    # TABLE_MARKER="<!-- TABLE_MARKER -->"
    # ADVENT_URL= "https://adventofcode.com"
    # STAR_SYMBOL = "<!--- advent_readme_stars table --->"
    # YEAR="2023,2022"
    import os
    from advent_readme_stars.constants import README_LOCATION, SESSION_COOKIE,  USER_ID, YEAR, ADVENT_URL,LEADERBOARD_ID,TABLE_MARKER
    from advent_readme_stars.advent import most_recent_advent_year
    

    
    # with open(README_LOCATION, "r") as f:
    #     lines = f.read().splitlines()

    # edited = update_readme(lines)

    # with open(README_LOCATION, "w") as f:
    #     for to_insert in edited:
    #         for line in to_insert:
    #             f.writelines([line + "\n"])
    
    def day_totime(day,year):
        d=datetime.datetime(year,12,day,10,0,0)
        return int(time.mktime(d.timetuple()))
    
    def timeconvert(membertime,day,year):
        unix=day_totime(int(day),int(year))
    
        datea = datetime.datetime.fromtimestamp(unix)
        dateb = datetime.datetime.fromtimestamp(membertime)
        return str(dateb-datea)
    def get_progress(y:str) -> dict:
        
        # print(y)
        if os.path.exists(f"{y}.json"):
            with open(f"{y}.json", 'r') as f:
                leaderboard_info=json.load(f)
        # with open(f"{y}.json", 'r') as f:
        #     leaderboard_info=json.load(f)
        # leaderboard_info["members"] = sorted(leaderboard_info['members'], key=lambda x : x['local_score'], reverse=True)
        members=""
        memb={}
        
        i=0
        for member,detail in leaderboard_info["members"].items():
            i+=1
           
            silverstartsymbol="⭐"
            # print(i,member,sc)
            stars = detail["completion_day_level"]
            if detail["name"]!=None and detail["local_score"]!=0:
                ft="| "+detail["name"] +" | " + str(detail["local_score"]) + " |" 
                for d in range(1,26):
                    parts=stars.get(str(d),{})
                    completed = parts.keys()
                    ft+= ("⭐"+timeconvert(parts["1"]["get_star_ts"],d,y) if "1" in completed else "     ") +  ("⭐"+timeconvert(parts["2"]["get_star_ts"],d,y) if "2" in completed else "     ") + " |"
                # for day, parts in stars.items():
                    # completed = parts.keys()
                    # for i in range(detail["stars"]):
                    #     ft+="⭐"
                    # ft+= ("⭐"+str(parts["1"]["get_star_ts"]) if "1" in completed else "     ") + " | " + ("⭐"+str(parts["2"]["get_star_ts"]) if "2" in completed else "     ") + " |"
                    # mb=Member(memberid=int(member),name=detail["name"],score=detail["local_score"],year=int(y),
                    #           dayProgress=DayProgress(
                    #         day=int(day),
                    #         part_1="1" in completed,
                    #         part_1ts=parts["1"]["get_star_ts"] if "1" in completed else -1 ,
                    #         part_2="2" in completed,
                    #         part_2ts=parts["2"]["get_star_ts"] if "2" in completed else -1,
                    #     ))
                    
                    # members.update(mb)
                    # members.append(mb)
                    # print(dp)
                members+=ft+"\n"
                memb.update({member:[detail["name"],detail["local_score"],ft]})
            # lines[:table_location] + ft + lines[table_location: ]
            
        return memb
    # print(get_progress(2023))
    
    # with open(f"2022.json", 'r') as f:
    #     f.readline()
        # leaderboard_info=json.load(f)
    
    def insert_table(lines: List[str]) -> List[str]: 
        # table_location = None
        # for i, line in enumerate(lines):
        #     if line.strip() == TABLE_MARKER:
        #         table_location = i
        #         break
        # else:
        #     return lines
        # print(table_location)
        
        to_insert=[  ]
        
        for y in YEAR.split(','):
            # print(y)
            toinsert = [
               f"## {y} Results"
            ]
            
            # return to_insert
            # break
            firstLine=f"| Name  | Score |"
            thirdLine="|:---:|:---:|"
            for day in range(1,26):
                day_url = f"{ADVENT_URL}/{y}/day/{day}"
                # firstLine += f"      [Day {day} {y}]({day_url})      |"
                firstLine += f"    [Day {day} {y}]({day_url})   |"
                thirdLine += ":---:|"
                
            
            
            toinsert.append(firstLine)
            # to_insert.append(secondLine)
            toinsert.append(thirdLine)
            
            # stars_info = sorted(dict(get_progress(y)), reverse=True)
            # print(stars_info.dayProgress.day)
            st= get_progress(y)
            data={key: val for key, val in sorted(st.items(), key = lambda ele: ele[1][1], reverse = True)}
            for key, val in data.items():
                # print(key, val[2])
                toinsert.append(val[2])
                # break
            # to_insert.append(st)
            # print(st)
            # return  lines[:table_location] + to_insert  
            # for key in st:
            #     # print(key)
            #     # break
            #     toinsert.append(key)
            
                # return  lines[:table_location] + to_insert + lines[table_location: ]
            # return  lines[:table_location] + to_insert + lines[table_location: ]
            # line=""
            # for star_info in stars_info:
            #     name=star_info.name
            #     score=star_info.score
               
            #     part_1_text = STAR_SYMBOL+ str(star_info.dayProgress.part_1ts) if star_info.dayProgress.part_1 else " "
            #     part_2_text = STAR_SYMBOL+ str(star_info.dayProgress.part_2ts) if star_info.dayProgress.part_2 else " "
             
            #     line+=f" | {part_1_text} | {part_2_text} |"
            # toinsert.append(f"| {name} | {score} {line} ")
            to_insert.append(toinsert)
        # print(toinsert)
        return lines+to_insert
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
    def update_readme(readme: List[str]) -> List[str]:
        """
        Take the contents of a readme file and update them
        """
        reduced = remove_existing_table(readme)
        
        new_readme = insert_table(reduced)
    
        return new_readme
    
    with open(README_LOCATION, "r" , encoding="utf-8") as f:
        lines = f.read().splitlines()
    edited = update_readme(lines)
    with open(README_LOCATION, "w", encoding="utf-8") as f:
        # f.writelines(edited)
        # f.write(f"{TABLE_MARKER}"+"\n")
        for to_insert in edited:
            # if type(to_insert)==list:
            #     for line in to_insert:
            #         f.writelines([line + "\n"])
            #     continue
            # else:
            #     print(type(to_insert),to_insert)
            # for line in to_insert:
                # print(type(line))
                # f.writelines([line + "\n"])
            # print(type(to_insert))
            
            if type(to_insert)==list:
                for line in to_insert:
                    f.writelines([line + "\n"])
            else:   
                f.writelines([to_insert + "\n"])
            
