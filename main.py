from common import *
from yt_wrapper import *
from yt_diff import makeYtSortDiff, S
from typing import Callable

def sortPlaylistBy(playlistId: str, key: Callable, default: S = 0, do_log=False):
    items = getPlaylistItems(playlistId)
    if do_log: log(items)
    diff = makeYtSortDiff(items, key, default)
    print(f"diff: {len(diff)}")
    for i, current_i, desired_i in diff:
        setPlaylistItemPosition(items[i], desired_i)

def sortBy(item):
    # TODO: get video length # contentDetails.duration?
    return (get(item, "contentDetails.endTime"), get(item, "snippet.videoOwnerChannelTitle"))

SORT_BY_DEFAULT = (0, "")

if __name__ == "__main__":
    build_youtube_api(True)
    sortPlaylistBy("PLei7IY8RpepzChsRJLiZzDl7xZugOdNPs", lambda item: get(item, "snippet.videoOwnerChannelTitle"), "", do_log=True)
    sortPlaylistBy("PLei7IY8Rpepxc1Dc_dTk3n9szAtehB0tZ", lambda item: get(item, "snippet.videoOwnerChannelTitle"), "")
    sortPlaylistBy("PLei7IY8Rpepwq7KXnsAbCgy83zb0KJxCh", lambda item: get(item, "snippet.videoOwnerChannelTitle"), "")
    sortPlaylistBy("PLei7IY8RpepwHukggpeEhrfBsf1s1S1rP", lambda item: get(item, "snippet.videoOwnerChannelTitle"), "")
    sortPlaylistBy("PLei7IY8Rpepw-DOu-ktuGE12xHMh78sro", lambda item: get(item, "snippet.videoOwnerChannelTitle"), "")
