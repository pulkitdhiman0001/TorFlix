from models import Files


def history(download_torrents_history, torrents, DownloadedTorrentList, get_user_identity):
    torrent_history = []
    for torrent in download_torrents_history:
        get_torrent = torrents.info(torrentId=torrent.torrent_id)

        get_torrent["torrentId"] = torrent.torrent_id

        get_torrent['user_id'] = get_user_identity
        get_torrent['ss'] = get_torrent["images"]

        torrent_history.append(get_torrent)

    return torrent_history


def currently_downloading(download_in_progress, torrents, DownloadedTorrentList, get_user_identity):
    downloading = []
    for torrent in download_in_progress:
        get_torrent = torrents.info(torrentId=torrent.torrent_id)
        get_torrent["torrentId"] = torrent.torrent_id
        get_torrent['ss'] = get_torrent["images"]
        get_downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=get_torrent["torrentId"]).first()
        if get_downloaded_torrent:
            get_torrent['downloaded_path'] = get_downloaded_torrent.downloaded_path

            get_torrent['email'] = get_user_identity

        downloading.append(get_torrent)

    return downloading
