import subprocess
import os

from models import Files, db


def audio_conversion(file_id, input_file, output_file, ext):
    if not ext == 'mp3':
        if os.path.exists(input_file):
            print("yes")
        else:
            print("no")
        try:


            print(input_file, '--------------')
            subprocess.run(['lame', '--preset', 'standard', str(input_file), str(output_file)])
            print(f"Conversion complete: {input_file} -> {output_file}")
            os.remove(input_file)
            get_file = Files.query.filter_by(id=file_id).first()
            get_file.file_path = output_file
            db.session.commit()
            return output_file.split('static/')[1]
        except Exception as e:
            print(f"Conversion failed: {e}")

    else:
        # print(input_file, 'input file path')
        return input_file
