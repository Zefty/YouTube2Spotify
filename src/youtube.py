# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from pathlib import Path
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class YoutubeClient:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "client_secret.json"
        self.get_credentials()
        self.build_youtube_client()

    def get_credentials(self):
        try:
            with open("credentials.pkl", "rb") as inp:
                self.credentials = pickle.load(inp)
            try:
                self.build_youtube_client()
                request = self.youtube.channels().list(
                    part="snippet,contentDetails,statistics", mine=True
                )
                _ = request.execute()
            except Exception:
                Path("credentials.pkl").unlink()
                self.get_credentials()
        except FileNotFoundError:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

            # Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, self.scopes
            )
            self.credentials = flow.run_console()
            with open("credentials.pkl", "wb") as outp:
                pickle.dump(self.credentials, outp, pickle.HIGHEST_PROTOCOL)

    def build_youtube_client(self):
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=self.credentials
        )

    def get_channel_playlists(self):

        playlists = {}

        request = self.youtube.playlists().list(
            part="snippet,contentDetails", maxResults=50, mine=True
        )
        response = request.execute()
        for pl in response["items"]:
            playlists[pl["snippet"]["title"]] = pl["id"]

        while response.get("nextPageToken", False):
            request = self.youtube.playlists().list(
                part="snippet,contentDetails",
                maxResults=50,
                mine=True,
                pageToken=response["nextPageToken"],
            )
            response = request.execute()
            for pl in response["items"]:
                playlists[pl["snippet"]["title"]] = pl["id"]

        return playlists

    def get_playlist_items(self, selected_playlist_id, path):
        def file_exists(file_name, path):
            for f in path.iterdir():
                if f.is_file():
                    if file_name in f.name:
                        return True
            return False

        playlist_items = []

        request = self.youtube.playlistItems().list(
            part="snippet", maxResults=50, playlistId=selected_playlist_id
        )
        response = request.execute()
        for pli in response["items"]:
            if not file_exists(pli["snippet"]["title"], path):
                playlist_items.append(
                    "https://www.youtube.com/watch?v={}".format(
                        pli["snippet"]["resourceId"]["videoId"]
                    )
                )

        while response.get("nextPageToken", False):
            request = self.youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                playlistId=selected_playlist_id,
                pageToken=response["nextPageToken"],
            )
            response = request.execute()
            for pli in response["items"]:
                if not file_exists(pli["snippet"]["title"], path):
                    playlist_items.append(
                        "https://www.youtube.com/watch?v={}".format(
                            pli["snippet"]["resourceId"]["videoId"]
                        )
                    )

        return playlist_items

