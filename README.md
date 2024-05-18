# Plex Delete Script
This script deletes series/movies that no one has watched within a specified number of days.
It uses Tautulli for statistics and Sonarr/Radarr for deleting. This way, series are also deleted from Sonarr, so that after deleting, everybody can easily request the same content via (I use Overseerr).

## Requirements
- Python
- Pip

## Setup

#### 1. Clone repository and change directory
```
git clone https://github.com/bbara04/Plex-Delete-Script.git
cd Plex-Delete-Script
```

#### 2. Install dependencies
```
pip install -r requirements.txt
```

#### 3. Configure script


Config.json

```json
{
    "local_ip_address": "localhost",                 Ip of the server these services run on.
    "plex": {
        "port": 32400,                               Plex port default is 32400.
        "api": "api"                                 Plex api.
    },
    "tautulli": {
        "port": 8181,                                Tautulli port default is 8181.
        "api": "api"                                 Tautulli api.
    },
    "sonarr": {
        "delete_after_days": 30,                     Number of days after unwatched series get deleted.
        "port": 8989,                                Sonarr port default is 8989.
        "api": "api"                                 Sonarr api.
    },
    "radarr": {
        "delete_after_days": 30,                     Number of days after unwatched movies get deleted.
        "port": 7878,                                Radarr port default is 7878.
        "api": "api"                                 Radarr api.
    },
    "excluded_lines": ["test"]                       Excluded words in the medias file path.
}
```

#### 4. Run script

```bash
python cleaner.py
```
