import os
import io
import zipfile
from PIL import Image

INPUT_ZIP = ".\\archive.zip"
OUTPUT_ZIP = ".\\recyscan_imges.zip"
TARGET_SIZE = (200, 200)
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

def is_image(filename):
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXT

with zipfile.ZipFile(INPUT_ZIP, 'r') as zin, \
     zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zout:

    for item in zin.infolist():
        if item.is_dir():
            zout.writestr(item.filename, "")
            continue

        data = zin.read(item.filename)

        if is_image(item.filename):
            try:
                img = Image.open(io.BytesIO(data))
                img.thumbnail(TARGET_SIZE, Image.LANCZOS)

                buf = io.BytesIO()
                img.save(buf, format=img.format if img.format else "PNG")
                buf.seek(0)

                zout.writestr(item.filename, buf.read())
            except Exception as e:
                print(f"Skipping {item.filename}: {e}")
                zout.writestr(item.filename, data)  # fallback: copy original
        else:
            zout.writestr(item.filename, data)

print("✅ Done! Saved resized zip as:", OUTPUT_ZIP)
