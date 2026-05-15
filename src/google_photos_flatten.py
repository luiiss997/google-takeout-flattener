from config import *
import json
import shutil
from datetime import datetime


# ===== EXTENSIONES PREDETERMINADAS =====

PHOTO_EXTENSIONS = {
    ".jpg", ".jpeg", ".png",
    ".heic", ".gif", ".bmp"
}

VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".avi", ".mkv"
}

# =========================

DEST_DIR.mkdir(
    parents=True,
    exist_ok=True
)

known_urls = set()

photo_files = []
video_files = []

duplicates = 0
skipped = 0
moved = 0

print("Escaneando archivos .JSON...")
for json_file in SOURCE_DIR.rglob("*.json"):
    try:
        with open(
            json_file,
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        title = data.get(
            "title"
        )

        url = data.get(
            "url"
        )

        timestamp = (
            data
            .get(
                "photoTakenTime",
                {}
            )
            .get(
                "timestamp"
            )
        )

        if not title:
            continue

        if url in known_urls:
            duplicates += 1
            print(
                f"Duplicado: {title}"
            )
            continue

        known_urls.add(url)
        base_name = Path(title).stem
        matches = []

        for candidate in json_file.parent.iterdir():
            if not candidate.is_file():
                continue
            
            if candidate.suffix == ".json":
                continue
            
            if base_name in candidate.stem:
                matches.append(candidate)

        if not matches:
            skipped += 1
            print(
                f"No encontrado: {title}"
            )
            continue

        # tomar el primero encontrado
        file_path = matches[0]

        extension = (
            file_path
            .suffix
            .lower()
        )

        if (
            extension not in PHOTO_EXTENSIONS
            and
            extension not in VIDEO_EXTENSIONS
        ):
            skipped += 1
            continue

        if timestamp:
            date = datetime.fromtimestamp(
                int(timestamp)
            )
        else:
            date = datetime.min

        data_tuple = (
            file_path,
            date
        )

        if extension in PHOTO_EXTENSIONS:
            photo_files.append(
                data_tuple
            )
        else:
            video_files.append(
                data_tuple
            )

    except Exception as e:
        print(
            f"Error {json_file.name}"
        )
        print(e)

print("Ordenando...")
photo_files.sort(
    key=lambda x: x[1]
)
video_files.sort(
    key=lambda x: x[1]
)

photo_counter = 1

for file, date in photo_files:
    extension = (
        file.suffix
        .lower()
    )

    new_name = (
        f"{BACKUP_PREFIX}"
        f"_IMG"
        f"{photo_counter:04d}"
        f"{extension}"
    )

    destination = (
        DEST_DIR
        / new_name
    )

    if not file.exists():
        print(
            f"Ya procesado: {file.name}"
        )
        continue

    shutil.move(
        str(file),
        str(destination)
    )

    print(
        f"Foto -> {new_name}"
    )

    moved += 1
    photo_counter += 1

video_counter = 1

for file, date in video_files:
    extension = (
        file.suffix
        .lower()
    )
    new_name = (
        f"{BACKUP_PREFIX}"
        f"_VID"
        f"{video_counter:04d}"
        f"{extension}"
    )

    destination = (
        DEST_DIR
        / new_name
    )

    if not file.exists():
        print(
            f"Ya procesado: {file.name}"
        )
        continue

    shutil.move(
        str(file),
        str(destination)
    )

    print(
        f"Video -> {new_name}"
    )

    moved += 1
    video_counter += 1

print("\nLimpiando archivos sobrantes...")
deleted_files = 0
deleted_folders = 0

# borrar archivos restantes
for file in SOURCE_DIR.rglob("*"):
    if file.is_file():
        try:
            file.unlink()
            deleted_files += 1
            print(
                f"Archivo eliminado: {file.name}"
            )
        except Exception as e:
            print(
                f"No se pudo borrar: {file}"
            )
            print(e)

print("\nEliminando carpetas...")
for folder in sorted(
    SOURCE_DIR.rglob("*"),
    reverse=True
):
    if folder.is_dir():
        try:
            folder.rmdir()
            deleted_folders += 1
            print(
                f"Carpeta eliminada: {folder.name}"
            )
        except:
            pass

print("\n===== LIMPIEZA =====")
print(
    f"Archivos eliminados: {deleted_files}"
)
print(
    f"Carpetas eliminadas: {deleted_folders}"
)

print(
    "\n===== TERMINADO ====="
)
print(
    f"Movidos: {moved}"
)
print(
    f"Duplicados: {duplicates}"
)
print(
    f"Ignorados: {skipped}"
)