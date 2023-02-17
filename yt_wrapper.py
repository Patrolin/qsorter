__all__ = ["build_youtube_api", "getPlaylistItems", "setPlaylistItemPosition"]

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import HttpRequest
from typing import Protocol, cast, Any
from common import *
from common import _get_step

youtube: Any = None

def build_youtube_api(oauth: bool):
    global youtube
    # https://console.cloud.google.com/apis/credentials
    with open("api_key.txt") as f:
        BASIC_YOUTUBE_KEY = f.read().strip() # presumably can't access private data
        print(f"BASIC_YOUTUBE_KEY: {BASIC_YOUTUBE_KEY}")

    credentials = None
    if oauth:
        OAUTH_SCOPES = [
            "https://www.googleapis.com/auth/youtube",
        ]
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=OAUTH_SCOPES)
        flow.run_local_server(timeout_seconds=300)
        credentials = flow.credentials
        print(f"credentials: {credentials}")

    # https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md
    youtube = build("youtube", "v3", developerKey=BASIC_YOUTUBE_KEY, credentials=credentials)

# https://developers.google.com/youtube/v3/docs
def cursed_get(value, path: str):
    steps = path.split(".")
    for step in steps[:-1]:
        value = _get_step(value, step)()
    return _get_step(value, steps[-1])

class GoogleFetch(Protocol):
    def __call__(self, part: str, **kwargs: Any) -> HttpRequest:
        ...

def request(path: str, part: str, **kwargs) -> Any:
    api = cast(GoogleFetch, cursed_get(youtube, path))
    return api(part=part, **kwargs).execute()

# bindings
def getPlaylistItems(playlistId: str, maxResults=50, **kwargs):
    items = []
    pageToken = None
    while True:
        response = request("playlistItems.list",
                           part="id,snippet,status",
                           playlistId=playlistId,
                           maxResults=maxResults,
                           **kwargs,
                           pageToken=pageToken)
        items.extend(response["items"])
        pageToken = getOrNone(response, "nextPageToken")
        if pageToken == None: break
    log(items)
    return items

def setPlaylistItemPosition(item, position: int):
    snippet = {
        "playlistId": get(item, "snippet.playlistId"),
        "resourceId": get(item, "snippet.resourceId"),
        "position": position,
    }
    body = {"id": get(item, "id"), "snippet": snippet}
    response = request("playlistItems.update", part="snippet", body=body)
    return response
