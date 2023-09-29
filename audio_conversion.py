import subprocess
import os

from models import Files, db


def audio_conversion(file_id, input_file, output_file, ext):
    if not ext == 'mp3':
        try:

            subprocess.run(['lame', '--preset', 'standard', str(input_file), str(output_file)])
            os.remove(input_file)
            get_file = Files.query.filter_by(id=file_id).first()
            get_file.file_path = output_file
            db.session.commit()
            return output_file.split('static/')[1]
        except Exception as e:
            print(f"Conversion failed: {e}")

    else:
        return input_file
