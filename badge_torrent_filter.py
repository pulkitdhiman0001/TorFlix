# def badge_filter_torrents(torrents, badge):
#
#     get_trending = torrents.trending()
#
#     items = get_trending["items"]
#
#     torrent_list = []
#
#     for torrent in items:
#         if torrent['genre'] == "badge":
#             torrent_info = torrents.info(torrent["link"])
#
#             torrent_list.append(torrent)
#
#     print(torrent_list)