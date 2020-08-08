import os

from dotenv import find_dotenv, load_dotenv
from googleapiclient.discovery import build

from src.config import YOUTUBE_API_VERSION, YOUTUBE_SERVICE_NAME

class YouTube:
    def __init__(self):
        self.env_file = find_dotenv()
        if not self.env_file:
            raise EnvironmentError("Could not load Spotify environment variables. Please, "
                                   "make sure a env variables are available")
        load_dotenv(self.env_file)
        self.key = os.getenv('YOUTUBE_DEV_KEY')
        self.service_name = YOUTUBE_SERVICE_NAME
        self.api_version = YOUTUBE_API_VERSION
        self.youtube_client = build(self.service_name, self.api_version, developerKey=self.key)

    def get_song_tags(self, name):
        video_id = self.search(name)
        video_details = self.youtube_client.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        return video_details['items'][0]['snippet']['tags']

    def search(self, name):
        request = self.youtube_client.search().list(
            q=name,
            part='id,snippet',
            maxResults=1
        ).execute()
        video_id = request['items'][0]['id']['videoId']
        return video_id
