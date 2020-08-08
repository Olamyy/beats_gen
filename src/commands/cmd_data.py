from pprint import pprint

import click

from src.config import PLAYLIST_ID
from src.helpers.cmd import CMDHelper
from src.helpers.spotify import Spotify
from src.helpers.utils import write_playlist_meta_data, set_envs
from src.helpers.youtube import YouTube
from src.main import pass_config


@click.group()
@click.help_option()
@pass_config
def cli(ctx):
    """Pipeline Operations."""


@cli.command()
@click.option("--no_youtube_tag", '-vb', default=False,
              is_flag=True, help="Flag to ignore youtube tags")
@click.option("--playlist-id",
              default=PLAYLIST_ID,
              help="ID of the playlist to get data from")
@click.option("--path", help="Path to store metadata")
@pass_config
def get_metadata(ctx, playlist_id, no_youtube_tag=False, path=None):
    """
    Retrieves metadata from playlist
    :return:
    """
    spotify_service = Spotify(playlist_id=playlist_id)
    playlist_metadata = spotify_service.get_data_from_playlist()
    path = path or f"data/metadata_{playlist_id}.json"
    if not no_youtube_tag:
        youtube_service = YouTube()
        playlist_metadata['tags'] = youtube_service.get_song_tags(playlist_metadata['name'])
    pprint(playlist_metadata)
    write_playlist_meta_data(tracks=playlist_metadata, path=path)
    click.echo(f"Metadata successfully written to {path}")


@cli.command()
@click.option("--playlist-id",
              default=PLAYLIST_ID,
              help="URL of the playlist to get data from")
@click.option("--path", help="Path to store metadata")
@pass_config
def get_mp3(ctx, playlist_id, path=None):
    path = path or f"data/href_{playlist_id}.txt"
    spotify_service = Spotify(playlist_id=playlist_id)
    spotify_service.download_playlist(path)
    click.echo(f"Playlist tracks written to {path}")
