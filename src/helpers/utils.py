import json
import os


def write_playlist_meta_data(path, tracks):
    with open(path, 'w') as fp:
        json.dump(tracks, fp)

def set_envs():
    os.environ['SPOTIPY_CLIENT_ID'] = "f3a3e79c51344d0db5254f37586053b5"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "8d4ad0027fdc4adca9a9d8c5c301899c"
    return True

