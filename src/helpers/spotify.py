import os

import spotipy
import spotipy.oauth2 as oauth2

from dotenv import load_dotenv, find_dotenv

from src.config import SPOTIFY_FEATURE_CONFIDENCE, SPOTIFY_AUDIO_FEATURES_NOT_NEEDED_KEYS
from src.helpers.cmd import CMDHelper


class Spotify:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.env_file = find_dotenv()
        if not self.env_file:
            raise EnvironmentError("Could not load Spotify environment variables. Please, "
                                   "make sure a env variables are available")
        load_dotenv(self.env_file)
        self.token = self.generate_token()
        self.client = spotipy.Spotify(auth=self.token)

    @staticmethod
    def generate_token():
        """ Generate the token. Please respect these credentials :) """
        credentials = oauth2.SpotifyClientCredentials(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'))
        return credentials.get_access_token()

    def write_tracks(self, text_file, tracks):
        with open(text_file, 'a') as file_out:
            while True:
                for item in tracks['items']:
                    if 'track' in item:
                        track = item['track']
                    else:
                        track = item
                    try:
                        track_url = track['external_urls']['spotify']
                        file_out.write(track_url + '\n')
                    except KeyError:
                        print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
                # 1 page = 50 results
                # check if there are more pages
                if tracks['next']:
                    tracks = self.client.next(tracks)
                else:
                    break

    @staticmethod
    def validate_confidence(track_feature):
        valid_confidences = []

        def confidence_greater_than(track, sub_check):
            check_collation = []
            for confidence in track[sub_check]:
                if confidence['confidence'] >= SPOTIFY_FEATURE_CONFIDENCE:
                    check_collation.append(confidence)
            return check_collation

        def convert_features_to_list(features, sub_check):  # Lol. I'm not proud of this but it works so I'm just going to leave it.
            """
            Hack to convert dict of features to a single list.
            :param features:
            :param sub_check:
            :return:
            """
            output = {}
            for r in features:
                for k, v in r.items():
                    if k in output:
                        output[k].append(v)
                    else:
                        output[k] = [v]

            return {
                sub_check: output
            }

        checks = ['bars', 'beats']  # Might be too much to get everything so I'm trying to get specific entries.
        for check in checks:
            analysis = confidence_greater_than(track_feature, sub_check=check)
            list_output = convert_features_to_list(analysis, sub_check=check)
            valid_confidences.append(list_output)

        return valid_confidences

    @staticmethod
    def clean_audio_features(features):
        for not_needed_key in SPOTIFY_AUDIO_FEATURES_NOT_NEEDED_KEYS:
            features.pop(not_needed_key)
        return features

    def get_data_from_playlist(self):
        results = self.client.playlist_tracks(self.playlist_id)
        items = results['items']
        track_details = {}
        for track in items[:1]:
            track_details['audio_analysis'] = self.validate_confidence(self.client.audio_analysis(track['track']['id']))
            track_details['audio_features'] = self.clean_audio_features(self.client.audio_features(track['track']['id'])[0])
            track_details['name'] = track['track']['name']
            track_details['artist'] = [artist['name'] for artist in track['track']['artists']]

        return track_details

    def write_track_href_to_file(self):
        results = self.client.playlist(self.playlist_id)
        text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
        print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
        tracks = results['tracks']
        self.write_tracks(text_file, tracks)

    def get_playlist_url(self):
        playlist = self.client.playlist(self.playlist_id)
        return playlist['external_urls']['spotify']

    def download_playlist(self, path):
        playlist_href = self.get_playlist_url()
        cmd_helper = CMDHelper()
        output = cmd_helper.run_cmd_command(
            [
                "spotify_dl", "-l", playlist_href, "-o", path
            ]
        )
        print(output)
