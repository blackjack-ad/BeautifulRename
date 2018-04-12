import sys
import datetime
import os
import tmdbsimple as tmdb
import requests
import simplejson as json

tmdb.API_KEY = 'XXXXXXXXXXXXXXXX'


def main():

    # String time
    time_begin = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

    print("Start of processing [" + time_begin + "]\n")

    input_filename = sys.argv[1]    # Directory principale Serie

    id_TVDB = sys.argv[2]   # ID della Serie TV su TBDB

    try:
        log_file = sys.argv[3]  # File di log per modifiche
    except:
        log_file = 'log_' + id_TVDB # File di log per modifiche automatico

    try:
        listdir = os.listdir(input_filename) # Lista di directory
    except:
        print("Error: The specified path could not be found: " + input_filename + "\nSpecifies a valid directory")
        exit()

    title_serietv = getNameTVserie(id_TVDB)

    print("TV Series: " + title_serietv + "\n")

    with open(log_file, 'w') as log:

        for dir in listdir:

            listfile = os.listdir(input_filename+"/"+dir)  # Lista di file (episodi)

            for file in listfile:
                path_file = input_filename+"/"+dir+"/"+file
                name_file = os.path.basename(path_file)

                episode_number = searchEpisode(name_file)  # Individua numero episodio

                title = [id_TVDB, episode_number]

                name_episode = searchNameEpisode(title)

                title_string = title_serietv + ' - ' + episode_number + ' - ' + name_episode

                new_path_file = path_file.replace(name_file, title_string)
                log.write(path_file + " -> " + new_path_file + '\n')
                print(title_string+'\n')

                os.rename(path_file, path_file.replace(name_file, title_string))  # Rinomina il file (ATTENZIONE)

    time_end = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    print("\nDone [" + time_end + "]")


def searchEpisode(s):

    pattern = generatePattern() # genera un dizionario del tipo {1x1: [varie combinazioni] ...}
    values = []
    keys = pattern.keys()

    for k in keys:
        values = pattern[k] # Lista di patterns per una chiave k
        for v in values:
            result = s.find(v)
            if result >= 0:
                s1 = k
                return s1
    return "?x?"


def generatePattern():

    pattern = {}

    # Chiavi
    keys = [str(x) + 'x' + str(y).zfill(2) for x in range(1, 21) for y in
            range(1, 31)]  # Lista ['1x1', '1x2' ... ] 20 stagione per 30 episodi

    # Simboli
    simboli = ['x', 'X', 'e', 'E', 'ep', 'EP']

    stagioni = [['1', '01'], ['2', '02'], ['3', '03'], ['4', '04'], ['5', '05'], ['6', '06'], ['7', '07'], ['8', '08'],
                ['9', '09'], ['10'], ['11'], ['12'], ['13'], ['14'], ['15'], ['16'], ['17'], ['18'], ['19'], ['20'],
                ['21']]

    episodi = [['1', '01'], ['2', '02'], ['3', '03'], ['4', '04'], ['5', '05'], ['6', '06'], ['7', '07'], ['8', '08'],
               ['9', '09'], ['10'], ['11'], ['12'], ['13'], ['14'], ['15'], ['16'], ['17'], ['18'], ['19'], ['20'],
               ['21'], ['22'], ['23'], ['24'], ['25'], ['26'], ['27'], ['28'], ['29'], ['30'], ['31']]

    i = 0
    y = 0
    for k in keys:
        pattern[k] = [str(s) + x + str(e) for x in simboli for s in stagioni[i] for e in episodi[y]]
        y = y + 1
        if y >= 30:
            y = 0
            i = i + 1

    return pattern


def searchNameEpisode(title):

    try:
        episode_number = title[1].split("x")

        season = episode_number[0]
        episode = episode_number[1]

        id = str(title[0])

        url = "https://api.themoviedb.org/3/tv/"+id+"/season/"+season+"/episode/"+episode+"?api_key="+tmdb.API_KEY

        payload = "{}"
        response = requests.request("GET", url, data=payload)

        data = response.text

        d = json.loads(data)
        name_episode = (d['name'])

        return name_episode

    except:
        return ""


def getNameTVserie(id):

    try:
        url = "https://api.themoviedb.org/3/tv/" + id + "?api_key=" + tmdb.API_KEY

        payload = "{}"
        response = requests.request("GET", url, data=payload)

        data = response.text

        d = json.loads(data)
        name_serie = (d['name'])

        return name_serie

    except:
        print("Error: invalid ID. Get a valid ID on The Movie Database (https://www.themoviedb.org/)")
        exit()

main()