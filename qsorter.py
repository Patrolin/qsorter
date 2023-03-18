from common import *
from yt_wrapper import *
from yt_diff import makeYtSortDiff
from typing import Callable

def sortPlaylistBy(playlistId: str, key: Callable, do_log=False):
    items = getPlaylistItems(playlistId)
    if do_log: log(items)
    diff = makeYtSortDiff(items, key)
    print(f"diff: {len(diff)}")
    for i, current_i, desired_i in diff:
        setPlaylistItemPosition(items[i], desired_i)

def sortBy(item):
    # TODO: get video length # contentDetails.duration?
    return (get(item, "contentDetails.endTime"), get(item, "snippet.videoOwnerChannelTitle"))

def printDuplicates(playlistIds):
    acc = dict()
    for playlistId in playlistIds:
        for item in getPlaylistItems(playlistId):
            videoId = get(item, "snippet.resourceId.videoId")
            acc[videoId] = [*acc.get(videoId, []), playlistId]
    for k, v in acc.items():
        if len(v) > 1:
            print(f"multiple playlists for https://www.youtube.com/watch?v={k}: {v}")

HAPPY_GLITCH = "PLei7IY8RpepwerjpVs0eEAZ-V_ew7Mqyh"
GLITCH = "PLei7IY8RpepzChsRJLiZzDl7xZugOdNPs"
JOURNEY = "PLei7IY8Rpepxc1Dc_dTk3n9szAtehB0tZ"
CALM = "PLei7IY8RpepwHukggpeEhrfBsf1s1S1rP"
CHILL = "PLei7IY8Rpepw-DOu-ktuGE12xHMh78sro"
WTF = "PLei7IY8Rpepwq7KXnsAbCgy83zb0KJxCh"
SOMBER = "PLei7IY8RpepyQjEPQ95do2vus_2g5OZmx"
ALL_PLAYLISTS = [
    HAPPY_GLITCH, GLITCH, \
    JOURNEY, \
    CALM, CHILL, \
    SOMBER,
    WTF,
]

def getSortKey(item):
    channel_name = getOrNone(item, "snippet.videoOwnerChannelTitle") or ""
    video_name = getOrNone(item, "snippet.title") or ""
    return [channel_name, video_name]

if __name__ == "__main__":
    build_youtube_api(True)
    printDuplicates(ALL_PLAYLISTS)
    for playlistId in ALL_PLAYLISTS:
        sortPlaylistBy(playlistId, getSortKey, do_log=True)
