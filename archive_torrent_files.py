from zipfile import ZipFile


def archive_torrent(archive_filename, files_to_archive):
    with ZipFile(archive_filename, 'w') as zipObj:
        for file in files_to_archive:
            zipObj.write(file)

    print(f"Archive '{archive_filename}' created successfully.")
    archive_path = archive_filename
    return archive_path
