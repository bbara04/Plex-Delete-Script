import requests
import json
from reader import plex_reader, radarr_reader, sonarr_reader, tautilli_reader


def fileNameCrop(str):
    return str.split('/')[-1]

with open("config.json", "r") as f:
    data = json.load(f)

f.close()

# if file name contains any of these strings, it will be excluded from the list
excluded_str = data['excluded_lines']

# Get all the metadata from the Plex, Sonarr, Radarr and Tautulli libraries
tautulli_stats = tautilli_reader.readTautulli(data['local_ip_address'], data['tautulli']['port'], data['tautulli']['api'])
plex_stats = plex_reader.readPlex(data['local_ip_address'], data['plex']['port'], data['plex']['api'])
sonarr_stats = sonarr_reader.readSonarr(data['local_ip_address'], data['sonarr']['port'], data['sonarr']['api'])
radarr_stats = radarr_reader.readRadarr(data['local_ip_address'], data['radarr']['port'], data['radarr']['api'])

# List of media that will be deleted
sel_list = []

# Get all media that is expired meaning it has not been watched for a certain amount of days
for tautulli in tautulli_stats:
    for plex in plex_stats:
        if tautulli[0] == plex[0]:
            tiltott = False
            # Check if the file name contains any of the excluded strings
            for exc_str in excluded_str:
                if exc_str.lower() in plex[2].lower():
                    tiltott = True
                    break
            # Handle the case if the media is a show
            if tiltott == False and plex[3] == "show":
                for sonarr in sonarr_stats:
                    if fileNameCrop(sonarr[2]) == fileNameCrop(plex[2]) and tautulli[2] > data['sonarr']["delete_after_days"]:
                        print(f"{sonarr[1]} |\tLast watched: {tautulli[2]} days ago |\t {plex[2]}")
                        sel_list.append((sonarr[0], plex[2], "show"))
            # Handle the case if the media is a movie
            elif tiltott == False and plex[3] == "movie":
                for radarr in radarr_stats:
                    if fileNameCrop(radarr[2]) == fileNameCrop(plex[2]) and tautulli[2] > data['radarr']["delete_after_days"]:
                        print(f"{radarr[1]} |\tLast watched: {tautulli[2]} days ago |\t {plex[2]}")
                        sel_list.append((radarr[0], plex[2], "movie"))

print("Do you want to delete all? [y/n] > ", end="")
answer = input()

# Delete all media that is expired
if answer.lower() == "y" or answer.lower() == "yes":
    for media in sel_list:
        if media[2] == "show":
            response = requests.delete(f"http://192.168.1.163:8989/api/v3/series/{media[0]}?deleteFiles=true&addImportListExclusion=false&apikey=241b9ffdac3741a0a693d6a3fe224e46")
            if response.status_code == 200:
                print("DELETED > " + fileNameCrop(media[1]))
        elif media[2] == "movie":
            response = requests.delete(f"http://192.168.1.163:7878/api/v3/movie/{media[0]}?deleteFiles=true&addImportExclusion=false&apikey=c349f3b312484de7bb1799006f08a96a")
            if response.status_code == 200:
                print("DELETED > " + fileNameCrop(media[1]))

