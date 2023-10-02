import ffmpeg
import subprocess
import re
import os
from models import create_app, db, Torrents, DownloadedTorrentList, Files


def convert_to_mp4(input_path, output_path, torrent_id, filename, file_id):
    if input_path == output_path:
        output_path = output_path.replace(output_path.split('/')[-1], "converted" + output_path.split('/')[-1])

    get_torrent = DownloadedTorrentList.query.filter_by(torrent_id=torrent_id).first()
    get_torrent_form_torrents = Torrents.query.filter_by(torrent_id=torrent_id).first()
    get_files = Files.query.filter_by(torrent_fk=get_torrent.id).first()

    get_torrent.conversion_flag = True
    get_torrent_form_torrents.conversion_flag = True
    db.session.commit()

    try:
        cmd = [
            'ffmpeg',
            '-y',
            '-i', input_path,  # Input file path
            '-c:v', 'h264_nvenc',  # NVIDIA NVENC H.264 (AVC) hardware encoder
            '-pix_fmt', 'yuv420p',  # Standard pixel format for compatibility
            '-preset', 'fast',  # Adjust the preset for speed/quality balance

            '-c:a', 'aac',  # AAC audio codec for wide compatibility
            '-strict', 'experimental',  # Required for AAC audio codec
            '-b:a', '192k',  # Adjust audio bitrate as needed

            '-movflags', '+faststart',  # Move MOOV atom to the beginning for streaming
            output_path,
        ]

        # Start the FFmpeg process and capture its output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        total_duration = get_total_duration(input_path)  # Get the total duration of the input video

        while True:
            # Read FFmpeg output line by line
            line = process.stderr.readline()
            if not line:
                break

            # Search for progress information in the line
            if "time=" in line:
                time_str = line.split("time=")[1].split()[0]
                current_time = parse_time(time_str)
                progress_percentage = (current_time / total_duration) * 100
                print(progress_percentage)
                if get_torrent_form_torrents:
                    # get_torrent_form_torrents.conversion_details = f"Processing for your device: {progress_percentage:.2f}%"
                    get_torrent_form_torrents.conversion_details = f"{progress_percentage:.2f}%. Processing: {filename}"
                    get_torrent_form_torrents.conversion_percentage = progress_percentage
                    db.session.commit()

        get_torrent_form_torrents.conversion_percentage = 100
        db.session.commit()

        # update_file_path = output_path
        # get_files.file_path = update_file_path
        # db.session.commit()

        get_specific_file = Files.query.filter_by(id=file_id).first()

        update_file_path = output_path
        get_specific_file.file_path = update_file_path

        get_specific_file.conversion_flag = True
        db.session.commit()

        print("Conversion complete.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def get_total_duration(input_path):
    # Use FFprobe command to get the total duration of the input video
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_path,
    ]
    ffprobe_process = subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    total_duration = float(ffprobe_process.stdout.readline())
    return total_duration


def parse_time(time_str):
    parts = time_str.split(':')
    seconds_parts = parts[-1].split('.')
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
    minutes = int(parts[-2])
    hours = int(parts[-3]) if len(parts) == 3 else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return total_seconds
