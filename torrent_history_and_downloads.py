from models import Files

def history(download_torrents_history, torrents, DownloadedTorrentList, get_user_identity):
    torrent_history = []
    for torrent in download_torrents_history:
        get_torrent = torrents.info(torrentId=torrent.torrent_id)

        get_torrent["torrentId"] = torrent.torrent_id
        # get_downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=get_torrent["torrentId"]).first()
        # if get_downloaded_torrent:
        # get_torrent['downloaded_path'] = get_downloaded_torrent.downloaded_path
        get_torrent['user_id'] = get_user_identity
        get_torrent['ss'] = get_torrent["images"]

        # files = Files.query.order_by(Files.file_path).filter_by(torrent_fk=get_downloaded_torrent.id).all()

        # for file in files:
        # search["files" + str(downloaded_torrents.torrent_id)].append(str(os.path.join('static', downloaded_torrents.downloaded_path, file)))
        # search["files" + str(downloaded_torrents.torrent_id)].append({file.id: file.file_path})
        # movie_list.append(search)
        torrent_history.append(get_torrent)
        # get_torrent.update({'files': files})

        # torrent_history.append(get_torrent)

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
            get_torrent['user_id'] = get_user_identity

        downloading.append(get_torrent)

    return downloading
