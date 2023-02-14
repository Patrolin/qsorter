from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import HttpRequest
from pprint import pprint
from typing import Callable, Protocol, TypeVar, cast, Any
import json
from sys import argv

# https://console.cloud.google.com/apis/credentials
with open("api_key.txt") as f:
    BASIC_YOUTUBE_KEY = f.read().strip() # presumably can't access private data
    print(f"BASIC_YOUTUBE_KEY: {BASIC_YOUTUBE_KEY}")

if True:
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
def _get_step(value, step: str):
    try:
        return value[step]
    except (AttributeError, TypeError, KeyError):
        return getattr(value, step)

def get(value, path: str):
    try:
        for step in path.split("."):
            value = _get_step(value, step)
        return value
    except (AttributeError, TypeError, KeyError) as e:
        pprint(value)
        raise e

def getOrNone(value, path: str):
    try:
        for step in path.split("."):
            value = _get_step(value, step)
        return value
    except (AttributeError, TypeError, KeyError):
        return None

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

def log(data):
    with open("log.txt", "w+") as f:
        f.write(json.dumps(data, indent=2))

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

T = TypeVar("T")

def makeSortMapping(items: list[T], key: Callable[[T], int], default: Any = 0) -> list[int]:
    items_with_index = [(v, i) for i, v in enumerate(items)]
    sorted_items_with_index = sorted(items_with_index,
                                     key=lambda vi: key(vi[0])
                                     if getOrNone(vi[0], "status.privacyStatus") not in ["privacyStatusUnspecified"] else default)
    sort_mapping = [0] * len(items)
    for i, vi in enumerate(sorted_items_with_index):
        sort_mapping[vi[1]] = i
    return sort_mapping

def makeYtSortDiff(items: list[T], key: Callable[[T], int], default) -> list[tuple[int, int]]:
    diff: list[tuple[int, int]] = []
    corrections: list[tuple[int, int]] = []
    sort_mapping = makeSortMapping(items, key, default)
    for i in range(len(items)):
        current_i = i
        for left, right in corrections:
            current_i += (right <= current_i) * (current_i < left) - (left < current_i) * (current_i <= right)
        if current_i != sort_mapping[i]:
            diff.append((i, sort_mapping[i]))
            corrections.append((current_i, sort_mapping[i]))
    return diff

#items = getPlaylistItems("PLei7IY8RpepxpqY5MjG4Jt_valumlC2Aq")
#log(items)
#setPlaylistItemPosition(items[2], 0)

def sortPlaylistBy(playlistId: str, key: Callable, default: Any = 0):
    items = getPlaylistItems(playlistId)
    diff = makeYtSortDiff(items, key, default)
    print(f"diff: {diff}")
    for i, j in diff:
        setPlaylistItemPosition(items[i], j)

sortPlaylistBy(argv[1], lambda item: get(item, "snippet.videoOwnerChannelTitle"), "")
