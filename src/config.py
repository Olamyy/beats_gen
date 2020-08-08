import click

SPOTIFY_FEATURE_CONFIDENCE = 0.9
SPOTIFY_AUDIO_FEATURES_NOT_NEEDED_KEYS = ['duration_ms', 'key', 'mode', 'id', 'uri', 'track_href', 'analysis_url', 'type']

YOUTUBE_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

PLAYLIST_ID = "3mnSxGFuDofc7RtA9Dp8Aq"

RED = click.style("ERROR", fg="red")

GREEN = click.style("OK", fg="green")