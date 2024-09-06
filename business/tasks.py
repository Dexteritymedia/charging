from huey import crontab
from huey.contrib import djhuey as huey
from huey.contrib.djhuey import task, periodic_task


#Run manage.py run_huey to activate


seasons = ["2000", "2001", "2002", "2003", "2004", "2005",
             "2006", "2007", "2008", "2009", "2010",
             "2011", "2012", "2013", "2014", "2015",
             "2016", "2017", "2018", "2019", "2020",
             "2021", "2022", "2023", "2024"]

codes = ["abdce579", "639950ae", "157b7fee", "d9fdd9d9", "03ff5eeb", "2091c619", "5f232eb1",
         "f98930d1", "6f7e1f03", "422bb734",]

clubs = ["Palmeiras", "Flamengo","Bahia","Botafogo-RJ","Cruzeiro","Athletico-Paranaense",
         "Sao-Paulo","Red-Bull-Bragantino","Internacional","Atletico-Mineiro"]

@task(retries=3, retry_delay=60)
def scrape_club_history(season):
    
    data =[]
    club_data = f"https://fbref.com/en/squads/03ff5eeb/{season}/Cruzeiro-Stats"
    print(club_data)
    try:
        response = requests.get(club_data)
    except requests.RequestException as e:
        raise e
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table_overall = soup.find(id="matchlogs_for")
    if table_overall == None:
        print("Club data does not exist")
    else:
        row = table_overall.select("tbody tr")
        for j in row:
            row_rank = j.find_all("th")
            row_data = j.find_all("td")
            row = [i.text for i in row_rank + row_data]
            data.append(row+[season]+[season]+[season])

    return data
