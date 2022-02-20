from __future__ import unicode_literals
from pathlib import Path
from yt_dlp import YoutubeDL


class Y2SLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def download_to_mp3(playlist_items, path, ffmpeg_location="ffmpeg"):
    def finish_hook(d):
        if d["status"] == "finished":
            print("Done downloading, now converting to mp3 ...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{path}/%(title)s.%(ext)s",
        "write_all_thumbnails": True,
        "ignoreerrors": True,
        "ffmpeg_location": ffmpeg_location,
        "postprocessor_args": ["-id3v2_version", "3"],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {"key": "EmbedThumbnail",},
        ],
        # "exec": "rm {}",
        "logger": Y2SLogger(),
        "progress_hooks": [finish_hook],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist_items)


def clean_up_thumbnails(path):
    thumbnails = [
        f
        for f in path.iterdir()
        if f.is_file()
        and (
            f.suffix == ".jpg"
            or f.suffix == ".webp"
            or f.suffix == ".png"
            or f.suffix == ".webm"
        )
    ]
    for f in thumbnails:
        f.unlink()


def inspect_path(path):
    if type(path) is str:
        path = Path(path)
    if not path.exists():
        try:
            path.mkdir()
        except FileNotFoundError:
            path.mkdir(parents=True)

