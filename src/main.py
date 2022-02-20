import argparse
from pathlib import Path
import questionary
from youtube import YoutubeClient
from downloader import download_to_mp3, clean_up_thumbnails, inspect_path


def y2s():
    # Get args
    args = parse_args()

    # Make sure path exists to download files to
    inspect_path(args.path)

    # Get playlist items from selected playlist
    youtube = YoutubeClient()
    playlists = youtube.get_channel_playlists()
    selected_playlist = questionary.select("Select a Playlist", choices=playlists).ask()
    playlist_items = youtube.get_playlist_items(playlists[selected_playlist], args.path)

    # Download playlist items to mp3 and clean up residual thumbnails
    download_to_mp3(playlist_items, args.path)
    clean_up_thumbnails(args.path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", type=Path, default=Path().cwd(), help="Spotify local files path",
    )
    parser.add_argument(
        "--ffmpeg-path",
        type=Path,
        default=Path().cwd() / "ffmpeg",
        help="Path to ffmpeg executables",
    )
    return parser.parse_args()


if __name__ == "__main__":
    print(
        """
██    ██ ██████  ███████ 
 ██  ██       ██ ██      
  ████    █████  ███████ 
   ██    ██           ██ 
   ██    ███████ ███████                        
"""
    )
    y2s()
