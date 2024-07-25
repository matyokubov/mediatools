import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TCON

def update_mp3_files(folder_path, image_path, genre):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            audio = MP3(file_path, ID3=ID3)

            # Add ID3 tag if it doesn't exist
            if audio.tags is None:
                audio.add_tags()

            # Remove existing APIC (cover art) frames
            audio.tags.delall('APIC')

            # Add new cover art
            with open(image_path, 'rb') as img:
                audio.tags.add(
                    APIC(
                        encoding=3,  # 3 is for utf-8
                        mime='image/jpeg',  # image type
                        type=3,  # 3 is for the cover(front) image
                        desc='Cover',
                        data=img.read()
                    )
                )

            # Set genre
            audio.tags.delall('TCON')
            audio.tags.add(TCON(encoding=3, text=genre))

            # Save changes
            audio.save()

# Usage
folder_path = "path/to/folder"
image_path = "sample.jpg"
genre = "phonk" # As example
update_mp3_files(folder_path, image_path, genre)
