from .common import *
from .yt_wrapper import *
from .yt_diff import makeYtSortDiff
from typing import Callable
from sys import argv

def sortPlaylistBy(playlistId: str, key: Callable, default: S = 0):
    items = getPlaylistItems(playlistId)
    diff = makeYtSortDiff(items, key, default)
    print(f"diff: {len(diff)}")
    for i, current_i, desired_i in diff:
        setPlaylistItemPosition(items[i], desired_i)

if __name__ == "__main__":
    sortPlaylistBy(argv[1], lambda item: get(item, "snippet.videoOwnerChannelTitle"), "")
