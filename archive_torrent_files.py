from zipfile import ZipFile
import os
from flask import send_file


def archive_torrent(archive_filename, files_to_archive):
    # Open the ZIP archive file for writing
    # Create a ZipFile Object
    with ZipFile(archive_filename, 'w') as zipObj:
        # Add multiple files to the zip
        for file in files_to_archive:
            zipObj.write(file)

    print(f"Archive '{archive_filename}' created successfully.")
    archive_path = archive_filename
    return archive_path
