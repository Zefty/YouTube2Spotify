# YouTube2Spotify 

> A simple script for converting YouTube playlists to local files for Spotify offline play 

Do you have a playlist of songs (copyrighted remixes, bootlegs, etc) that are available only on YouTube, and wished to have them also on Spotify? 

YouTube2Spotify is a quick and simple script that converts your favourite songs on YouTube to a local/offline storage for Spotify. You can then create a playlist with the downloaded songs using the Spotify desktop client and later sync them to your phone! 

NOTE: Currently, the script is very simple and only downloads the selected playlist to the local path. You need to then create the playlist manually on Spotify and enable "download" to be able to sync to other devices (e.g. phone). 


### Dependencies 
```
pip install -r requirements.txt
```

The repo contains ffmpeg already so no need to pass the `--ffmpeg-path` argument. However, if you would like to use an alternatve version of ffmeg (e.g. linux), you can pass in the ffmeg path.  

NOTE: You need to create obtain a client_secret.json file from Google Cloud to use the Youtube API. 

### Example
```
python src/main.py --path <path_to_spotify_local_path> --ffmpeg-path <path_to_ffmpeg>
```
