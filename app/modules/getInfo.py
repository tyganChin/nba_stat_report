## Name    : getInfo.py
## Author  : Tygan Chin
## Purpose : Takes in a player id and generates a report for the player involving 
##           averges, totals, general info, teams, and awards. Report is saved to 
##           index.html.

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
from collections import namedtuple
from collections import defaultdict
from adjustText import adjust_text
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerawards
from nba_api.stats.endpoints import alltimeleadersgrids

with open("static/data/teamLogos.json", "r") as file:
    team_logos = json.load(file) 

# get player id
playerId = sys.argv[1]

# chosen player
commonInfo = ['PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 'DISPLAY_FIRST_LAST', 'DISPLAY_LAST_COMMA_FIRST', 'DISPLAY_FI_LAST', 'PLAYER_SLUG', 'BIRTHDATE', 'SCHOOL', 'COUNTRY', 'LAST_AFFILIATION', 'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'JERSEY', 'POSITION', 'ROSTERSTATUS', 'NULL', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CODE', 'TEAM_CITY', 'PLAYERCODE', 'FROM_YEAR', 'TO_YEAR', 'DLEAGUE_FLAG', 'NBA_FLAG', 'GAMES_PLAYED_FLAG', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER']
playerInfo = (commonplayerinfo.CommonPlayerInfo(player_id=playerId)).get_dict()
dataRows = playerInfo['resultSets'][0]['rowSet'][0]
playerData = dict(zip(commonInfo, dataRows))

# graph constants
Graph = namedtuple('Graph', ['title', 'xLabel', 'yLabel', 'fileName'])
Career_Pts = Graph('Career PPG', 'Season', 'PPG', 'careerPts_graph.png')
Career_Rebs = Graph('Career RPG', 'Season', 'RPG', 'careerRebs_graph.png')
Career_Asts = Graph('Career APG', 'Season', 'APG', 'careerAsts_graph.png')
Career_Stls = Graph('Career SPG', 'Season', 'SPG', 'careerStls_graph.png')
Career_Blks = Graph('Career BPG', 'Season', 'BPG', 'careerBlks_graph.png')
Career_Mins = Graph('Career MPG', 'Season', 'MPG', 'careerMins_graph.png')
Career_Tovs = Graph('Career TPG', 'Season', 'TPG', 'careerTovs_graph.png')
graphs = [Career_Pts, Career_Rebs, Career_Asts, Career_Stls, Career_Blks, Career_Mins, Career_Tovs]

# generates a lin graph and saves it to given file name
def setGraph(x, ys, graphInfo):
    plt.rcParams['font.family'] = 'Palatino'

    # Create the plot
    plt.plot(x, ys[2], label='League Leader', color=mainColor, marker='o', markersize=2)
    plt.plot(x, ys[0], label='Player', color=secondColor, marker='o', markersize=2)
    plt.plot(x, ys[1], linestyle='--', label='Average', color=mainColor, marker='o', markersize=2)

    # set label positions
    texts = []
    for y in ys:
        for i in range(len(x)):
            texts.append(plt.text(x[i], y[i], y[i], fontsize=10, ha='center', fontweight='bold'))

    # Adjust labels (send output to null)
    sys.stdout = open(os.devnull, 'w')
    adjust_text(texts)
    sys.stdout = sys.__stdout__

    # set other information
    plt.xticks(x, rotation=90)
    if (not np.nan in ys[2]):
        plt.ylim(0, max(ys[2]) + (max(ys[2]) * 0.1))
    plt.ylim(0)
    plt.tight_layout()
    plt.legend(loc='best')

    # save and close
    static_images_path = os.path.join(os.path.dirname(__file__), '../static/images/')
    plt.savefig(os.path.join(static_images_path, graphInfo.fileName), format='png')
    plt.close()

# gets the age of a person given their data of birth
def getAge(bday_str):
    curr = datetime.now().date()
    bday = datetime.strptime(bday_str, '%Y-%m-%dT%H:%M:%S')

    age = curr.year - bday.year
    if curr.month < bday.month or (curr.month == bday.month and curr.day < bday.day):
        age -= 1
    return age

# extracts and formats the draft year of a player
def getDraft(year, round, number):
    if year is None or round is None or number is None:
        return None
    elif year == 'Undrafted':
        return 'Undrafted'
    else:
        return year + " (r" + (round) + "/p" + (number) + ")"

# returns a 2 element list representing the years string given (XXXX-XX)
def makeYear(yr_str):
    start = yr_str[:4]
    if start[2:4] == "99":
        return [start, str(int(yr_str[:2]) + 1) + "00"]
    return [start, yr_str[:2] + yr_str[5:7]]

# get player carreer averges
headers = ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'Team_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
career = playercareerstats.PlayerCareerStats(player_id=playerId, per_mode36="PerGame").get_dict()
rows = career['resultSets'][0]['rowSet']
playerCareer = [dict(zip(headers, row)) for row in rows]

# get player career average totals
careerheaders = ['PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
row = career['resultSets'][1]['rowSet'][0]
careerAvgTotals = dict(zip(careerheaders, row))

# get player teams
teamList = [[playerCareer[0]['TEAM_ABBREVIATION'], makeYear(playerCareer[0]['SEASON_ID'])]]
for season in playerCareer[1:]:
    if season['TEAM_ABBREVIATION'] == teamList[-1][0]:
        teamList[-1][1][1] = makeYear(season['SEASON_ID'])[1]
    elif season['TEAM_ABBREVIATION'] != 'TOT':
        teamList.append([season['TEAM_ABBREVIATION'], makeYear(season['SEASON_ID'])])

# write player teams to html
teamHistory = ''
for team in teamList:
    teamHistory += f"<div class='team'> <div class='team-img-container'> <img class='team-img' src='{team_logos[team[0]] if team_logos.get(team[0]) is not None else 'https://logos-world.net/wp-content/uploads/2020/11/NBA-Logo.png'}'> </div> <div class='team-title'>{team[0]}</div> <div class='team-length'>{team[1][0] + '\n' + team[1][1]}</div></div>"

# set main team (will appear next to their logo and page will be themed based on this team)
if playerData['ROSTERSTATUS'] == 'Active':
    playerData['TEAM_ABBREVIATION'] = teamList[-1][0]
else:
    abr = teamList[0][0]
    amt = int(teamList[0][1][1]) - int(teamList[0][1][0])
    for team in teamList[1:]:
        if int(team[1][1]) - int(team[1][0]) >= amt:
            amt = int(team[1][1]) - int(team[1][0])
            abr = team[0]
    playerData['TEAM_ABBREVIATION'] = abr

# set the theme colors of the report based on players team
with open('static/data/teamColors.json', 'r') as file:
    team_colors = json.load(file) 
if playerData['TEAM_ABBREVIATION'] in team_colors:
    mainColor = team_colors[playerData['TEAM_ABBREVIATION']][0]
    secondColor = team_colors[playerData['TEAM_ABBREVIATION']][1]
else:
    mainColor = '#17408B'
    secondColor = '#C8102E'

# write general inforatiom to html
generalInfo = [['Position', playerData['POSITION']], ['Height', playerData['HEIGHT']], ['Team', playerData['TEAM_ABBREVIATION']], ['Age', getAge(playerData['BIRTHDATE'])], ['Draft', getDraft(playerData['DRAFT_YEAR'], playerData['DRAFT_ROUND'], playerData['DRAFT_NUMBER'])], ['School', playerData['SCHOOL']], ['Yrs Pro', playerData['SEASON_EXP']]]
generalInfo_HTML = ""
for info in generalInfo:
    generalInfo_HTML += f"<div class='infoRow'> <div class='label'>{info[0]}</div> <div class='value'>: {info[1] if info[1] is not None else 'N/A'}</div> </div>"

# calculate playoff totals
NAheaders = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
if len(career['resultSets'][2]['rowSet']) > 0:
    row = career['resultSets'][3]['rowSet'][0]
    playoffTotals = dict(zip(careerheaders, row))
else:
    playoffTotals = dict(zip(careerheaders, NAheaders))

# get league leaders and league averages
with open('static/data/leaders.json', 'r') as file:
    leaders = json.load(file)
with open('static/data/output.json', 'r') as file:
    averages = json.load(file)

# get player's awards
awardHeaders = ['PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 'TEAM', 'DESCRIPTION', 'ALL_NBA_TEAM_NUMBER', 'SEASON', 'MONTH', 'WEEK', 'CONFERENCE', 'TYPE', 'SUBTYPE1', 'SUBTYPE2', 'SUBTYPE3']
awards = playerawards.PlayerAwards(player_id=playerId).get_dict()
rows = awards['resultSets'][0]['rowSet']
playerAwards = [dict(zip(awardHeaders, row)) for row in rows]

# init award dictionary with predetermined order 
awardOrder = ['NBA Champion', 'NBA Most Valuable Player', 'NBA Finals Most Valuable Player', 'NBA All-Star', 'All-NBA 1st Team', 'All-NBA 2nd Team', 'All-NBA 3rd Team', 'Olympic Gold Medal']
awardDict = defaultdict(int)
for award in awardOrder:
    awardDict[award] += 0

# add award count to dictionary
ordinals = ['st', 'nd', 'rd']
for award in playerAwards:
    if award['DESCRIPTION'] == 'All-Defensive Team' or award['DESCRIPTION'] == 'All-Rookie Team':
        awardDict[award['DESCRIPTION'][:-4] + ' ' + award['ALL_NBA_TEAM_NUMBER'] + ordinals[int(award['ALL_NBA_TEAM_NUMBER']) - 1] + " Team"] += 1
    elif award['DESCRIPTION'] == 'All-NBA' or award['DESCRIPTION'] == 'All-Defensive Team' or award['DESCRIPTION'] == 'All-Rookie Team':
        awardDict[award['DESCRIPTION'] + ' ' + award['ALL_NBA_TEAM_NUMBER'] + ordinals[int(award['ALL_NBA_TEAM_NUMBER']) - 1] + " Team"] += 1
    else:
        awardDict[award['DESCRIPTION']] += 1

# create html to display awards
HTML_Awards = ""
for name, award in awardDict.items():
    if award != 0:
        HTML_Awards += f"<div class='award'> <div class='award-img'> <img id='award-img' src='static/images/trophy.png'> <div class='award-num'>{award}X</div></div> <div class='award-title'>{name}</div></div>"

# generate carreer average line graphs
averageButtons = ""
stats = [['PTS', 'careerPPGbutton', 1], ['REB', 'careerRPGbutton', 1], ['AST', 'careerAPGbutton', 1], ['STL', 'careerSPGbutton', 2], ['BLK', 'careerBPGbutton', 2], ['MIN', 'careerMPGbutton', 0], ['TOV', 'careerTPGbutton', 2]]
for i in range(len(stats)):
    x = [] 
    ys = [[], [], []]
    j = 0
    while j < len(playerCareer):
        while j + 1 < len(playerCareer) and playerCareer[j + 1]['SEASON_ID'] == playerCareer[j]['SEASON_ID']:
            j += 1

        if playerCareer[j][stats[i][0]] != None:
            ys[0].append(playerCareer[j][stats[i][0]])
        else:
            ys[0].append(np.nan)

        if str(i + 1) in averages[playerCareer[j]['SEASON_ID']]:
            ys[1].append(round(averages[playerCareer[j]['SEASON_ID']][str(i + 1)] / averages[playerCareer[j]['SEASON_ID']]["0"], stats[i][2]))
        else:
            ys[1].append(np.nan)

        if leaders[playerCareer[j]['SEASON_ID']][i] != 0:
            ys[2].append(leaders[playerCareer[j]['SEASON_ID']][i])
        else:
            ys[2].append(np.nan)

        x.append(playerCareer[j]['SEASON_ID'])
        j += 1

    averageButtons += f"<div>&nbsp;|&nbsp;</div> <div onclick='countingStatButtonClicked({i})' id={stats[i][1]} class='countingStatButton' style='text-decoration: {'underline' if i == 0 else 'none'}'>{stats[i][0]}</div>"
    setGraph(x, ys, graphs[i])
averageButtons += '<div>&nbsp;|&nbsp;</div>'

# write career, playoff, and current averges to html
careerAvgCategories = [['careerAverages', careerAvgTotals], ['playoffAverages', playoffTotals], ['currentAverages', playerCareer[-1]]]
careerLabels = [['PTS', 'PPG'], ['REB', 'RPG'], ['AST', 'APG'], ['STL', 'SPG'], ['BLK', 'BPG'], ['MIN', 'MPG'], ['TOV', 'TPG'], ['FG_PCT', 'FG%'], ['FT_PCT', 'FT%'], ['FG3_PCT', '3P%']]
careerAvgs_HTML = ""
for id, dic in careerAvgCategories:
    careerAvgs_HTML += f'<div class="average-container" id="{id}" style="display: {'grid' if id == 'careerAverages' else 'none'};">'
    for key, label in careerLabels:
        careerAvgs_HTML += f'<div class="average" style="border: 1px solid {secondColor};"> <div style="border-bottom: 1px solid {secondColor};"class="average-title"> <p>{label}</p></div> <div class="average-value"> <p>{round(dic[key], 2) if dic.get(key) is not None else 'N/A'} </p> </div> </div>'
    careerAvgs_HTML += f'</div>'

# write season average graphs to html
careerAvgGraphs = [['careerPts', 'careerPts_graph.png'], ['careerRebs', 'careerRebs_graph.png'], ['careerAsts', 'careerAsts_graph.png'], ['careerStls', 'careerStls_graph.png'], ['careerBlks', 'careerBlks_graph.png'], ['careerMins', 'careerMins_graph.png'], ['careerTovs', 'careerTovs_graph.png']]
careerGraphs_HTML = ''
for id, fileName in careerAvgGraphs:
    careerGraphs_HTML += f'<img style="display: {"flex" if id == "careerPts" else "none"};" id="{id}" src="{{{{ url_for(\'static\', filename=\'images/{fileName}\') }}}}">'


# get career total amoutns for player
careerTotalAmts = playercareerstats.PlayerCareerStats(player_id=playerId, per_mode36="Totals").get_dict()
row = careerTotalAmts['resultSets'][1]['rowSet'][0]
careerTotals = dict(zip(careerheaders, row))

# get all time leader lists for each category
alltimeleaders = alltimeleadersgrids.AllTimeLeadersGrids(league_id="00", per_mode_simple = "Totals", season_type="Regular Season", topx="10000").get_dict()
leagueLeaders = {}
for sets in alltimeleaders['resultSets']:
    leagueLeaders.setdefault(sets['name'], []).extend(sets['rowSet'])

# finds the rank of a player all time for a particular stat and returns the index
def findPlayer(leaders, start, end, val):
    mid = int((start + end) / 2)
    if val < leaders[mid][2]:
        return findPlayer(leaders, mid + 1, end, val)
    elif val > leaders[mid][2]:
        return findPlayer(leaders, start, mid, val)
    else:
        i = 0
        while (mid + i < len(leaders) and int(playerId) != leaders[mid + i][0]) and (mid - i >= 0 and int(playerId) != leaders[mid - i][0]):
            i += 1
        return mid + i if mid + i < len(leaders) and int(playerId) == leaders[mid + i][0] else mid - i

# set bar graph representing players rank all-time for a particular stat
def setBarGraph(x, y, rank, graphInfo):

    # set label positions
    playerInd = 0
    texts = []
    for i in range(len(x)):
        texts.append(plt.text(x[i], y[i], y[i], fontsize=12, ha='center', fontweight='bold'))
        if x[i] == leagueLeaders[barGraph.leadersKey][ind][1].replace(" ", "\n"):
            playerInd = i

    # Create the plot
    colors = [mainColor] * 5
    colors[playerInd] = secondColor
    plt.bar(x, y, color=colors)
    
    # set y-axis limits
    if (not np.nan in y):
        plt.ylim(min(y) - (0.01 * max(y)), (max(y) * 1.009))

    # set rank label
    yticks = plt.yticks()[0]
    tick_step = yticks[2] - yticks[1] 
    texts.append(plt.text(x[playerInd], y[playerInd] - tick_step / 2, 'Rank: ' + str(rank), fontsize=10, ha='center', fontweight='bold', color='white'))

    # Set given information
    plt.xticks(x)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.rcParams['font.family'] = 'Palatino'

    # close and save plot
    static_images_path = os.path.join(os.path.dirname(__file__), '../static/images/')
    plt.savefig(os.path.join(static_images_path, graphInfo.fileName), format='png')
    plt.close()

# bar graph constants
barGraph = namedtuple('barGraph', ['leadersKey', 'xLabel', 'yLabel', 'fileName', 'careerKey', 'id', 'buttonId'])
barGraphInfo = [
    barGraph('PTSLeaders', 'Players', 'PTS', 'careerPts_bargraph.png', 'PTS', 'totalCareerPts', 'totalCareerPts_button'), 
    barGraph('REBLeaders', 'Players', 'REBS', 'careerRebs_bargraph.png', 'REB', 'totalCareerRebs', 'totalCareerRebs_button'), 
    barGraph('ASTLeaders', 'Players', 'ASTS', 'careerAsts_bargraph.png', 'AST', 'totalCareerAsts', 'totalCareerAsts_button'), 
    barGraph('STLLeaders', 'Players', 'STLS', 'careerStls_bargraph.png', 'STL', 'totalCareerStls', 'totalCareerStls_button'), 
    barGraph('BLKLeaders', 'Players', 'BLKS', 'careerBlks_bargraph.png', 'BLK', 'totalCareerBlks', 'totalCareerBlks_button'), 
    barGraph('TOVLeaders', 'Players', 'TOVS', 'careerTovs_bargraph.png', 'TOV', 'totalCareerTovs', 'totalCareerTovs_button')]

# set graphs to display players all time ranks
barGraph_HTML = ''
totalButtons_HTML = ''
for j in range(len(barGraphInfo)):
    barGraph = barGraphInfo[j]
    if careerTotals[barGraph.careerKey] == None:
        continue
    
    playerNames = [0] * 5
    playerTotals = [0] * 5
    ind = findPlayer(leagueLeaders[barGraph.leadersKey], 0, len(leagueLeaders[barGraph.leadersKey]) - 1, careerTotals[barGraph.careerKey])
    if ind + 3 > len(leagueLeaders[barGraph.leadersKey]):
        start = (len(leagueLeaders[barGraph.leadersKey]) - ind) - 1
    elif ind < 2:
        start = 4 - ind
    else:
        start = 2

    playerNames[start] = leagueLeaders[barGraph.leadersKey][ind][1].replace(" ", "\n")
    playerTotals[start] = leagueLeaders[barGraph.leadersKey][ind][2]

    i = 1
    while start - i >= 0:
        playerNames[start - i] = leagueLeaders[barGraph.leadersKey][ind + i][1].replace(" ", "\n")
        playerTotals[start - i] = leagueLeaders[barGraph.leadersKey][ind + i][2]
        i += 1
    i = 1
    while start + i < 5:
        playerNames[start + i] = leagueLeaders[barGraph.leadersKey][ind - i][1].replace(" ", "\n")
        playerTotals[start + i] = leagueLeaders[barGraph.leadersKey][ind - i][2]
        i += 1
    setBarGraph(playerNames, playerTotals, leagueLeaders[barGraph.leadersKey][ind][3], barGraph)
    barGraph_HTML += f'<img style="display: {'flex' if barGraph.id == 'totalCareerPts' else 'none'};" id="{barGraph.id}" src="{{{{ url_for(\'static\', filename=\'images/{barGraph.fileName}\') }}}}">'
    totalButtons_HTML += f"<div>&nbsp;|&nbsp;</div> <div onclick='totalStatButtonClicked({j})' id='{barGraph.buttonId}' class='countingStatButton' style='text-decoration: {'underline' if barGraph.careerKey == 'PTS' else 'none'}'>{barGraph.yLabel}</div>"
totalButtons_HTML += '<div>&nbsp;|&nbsp;</div>'

# write to html
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates', 'index.html')
with open(file_path, 'w') as f:
    f.write(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PlayerStats</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href= "/static/css/view.css">

    </head>
    <body id="body" style="background-color: {secondColor};">

        <img id="background-texture" src="static/images/paper-background.png" alt="background texture" id="background">

        <img id="loading" src="../static/images/loading.gif">

        <div style="background-color: {secondColor};" class="top-bar" id="top-bar">
            <img onclick="goHome()" id="logo" src={team_logos[playerData['TEAM_ABBREVIATION']] if team_logos.get(playerData['TEAM_ABBREVIATION']) is not None else 'https://logos-world.net/wp-content/uploads/2020/11/NBA-Logo.png'}>
            <p style="margin-left: 1%; text-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);">{playerData['DISPLAY_FIRST_LAST']}'s Report</p>
            <div class="search-container">
                <input class="searchBox" id="input" type="text" placeholder="Player" autocomplete="off">
                <div id="results-container"> </div>
            </div>
        </div>

        <div class='container' style="background-color: {mainColor};" id="main">

            <div class="row1">
                <div id="playerImage-container">
                    <img id="playerImage" src="https://cdn.nba.com/headshots/nba/latest/1040x760/{playerId}.png">
                    <div style="color: {secondColor};"id="playerNumber">{playerData['JERSEY']}</div>
                </div>
                
                <div id="playerInfo-container">
                    <div style="color: {secondColor};" id="playerInfo-title">General Info</div>
                    <div id="playerInfo">{generalInfo_HTML}</div>
                </div>

                <div class="averages-container">
                    <div class="averages-buttons">
                        <div onclick = "averagesButtonClicked(0)" class="averages-button" id="careeraverages-button" style="color: {secondColor}; text-decoration: underline;">Career</div>
                        <div>&nbsp;|&nbsp;</div>
                        <div onclick = "averagesButtonClicked(1)" class="averages-button" id="playoffaverages-button" style="color: {secondColor};">Playoff</div>
                        <div>&nbsp;|&nbsp;</div>
                        <div onclick = "averagesButtonClicked(2)" class="averages-button" id="currentaverages-button" style="color: {secondColor};">Current</div>
                    </div>
                    {careerAvgs_HTML}
                </div>
            </div>

            <div class="row2">
                <div class="graph-container">
                    <div style="color: {secondColor};" class="countingStatButtons">{averageButtons}</div>
                    {careerGraphs_HTML}
                </div>

                <div class="awards-teams-container">
                    <div class="awards-container">
                        <div style="color: {secondColor};" class="awards-title">Awards</div>
                        <div class="awards">{HTML_Awards}</div>
                    </div>

                    <div class="teams-container">
                        <div style="color: {secondColor};" class="teams-title">Teams</div>
                        <div class="teams">{teamHistory}</div>
                    </div>
                </div>

                <div class="graph-container">
                    <div style="color: {secondColor};" class="countingStatButtons">{totalButtons_HTML}</div>
                    {barGraph_HTML}
                </div>


            </div>
            <script src="static/js/statScript.js"></script>
        </div>

        <footer style="background-color: {secondColor};" class="footer" id="footer">
            <p style="text-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);">Copyright © Tygan Chin 2024</p>
        </footer>
    </body>
    </html>
    """)