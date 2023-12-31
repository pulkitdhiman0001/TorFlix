from models import DownloadedTorrentList


def get_torrent_details(items, torrents, category=None, badge=None):
    movie_list = []

    for movie in items:
        link = torrents.info(link=f'{movie["link"]}')
        get_downloaded_torrent = DownloadedTorrentList.query.filter_by(torrent_id=movie['torrentId']).first()
        if badge:

            if link['genre'] == "badge":
                if not get_downloaded_torrent and not link["category"] == "XXX" and not link[
                                                                                            "category"] == "Games" and not \
                        link["category"] == "Apps":

                    movie['thumbnail'] = link["thumbnail"]
                    movie['description'] = link['description']
                    movie['genre'] = link['genre']
                    if link["images"] is None:
                        movie['ss'] = 'None'

                    else:
                        movie['ss'] = link["images"]

                    if link['magnetLink'] is None:
                        movie['magnetLink'] = 'none'

                    else:
                        movie['magnetLink'] = link['magnetLink']

                    if link['category'] is None:
                        movie['category'] = '----'

                    else:
                        movie['category'] = link['category']

                    if link['type'] is None:
                        movie['type'] = '----'

                    else:
                        movie['type'] = link['type']

                    if link['language'] is None:
                        movie['language'] = '----'

                    else:
                        movie['language'] = link['language']
                        movie_list.append(movie)

        if not get_downloaded_torrent and not link["category"] == "XXX" and not link["category"] == "Games" and not \
                link["category"] == "Apps":
            link = torrents.info(link=f'{movie["link"]}')

            movie['thumbnail'] = link["thumbnail"]
            movie['description'] = link['description']
            movie['genre'] = link['genre']
            if link["images"] is None:
                movie['ss'] = 'None'

            else:
                movie['ss'] = link["images"]

            if link['magnetLink'] is None:
                movie['magnetLink'] = 'none'

            else:
                movie['magnetLink'] = link['magnetLink']

            if link['category'] is None:
                movie['category'] = '----'

            else:
                movie['category'] = link['category']

            if link['type'] is None:
                movie['type'] = '----'

            else:
                movie['type'] = link['type']

            if link['language'] is None:
                movie['language'] = '----'

            else:
                movie['language'] = link['language']
                movie_list.append(movie)

    return movie_list
