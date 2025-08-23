import zipfile
import os

def split_zip_by_files(zip_path, out_dir, max_size_mb=200):
    with zipfile.ZipFile(zip_path, 'r') as zin:
        files = zin.infolist()

    os.makedirs(out_dir, exist_ok=True)
    batch = []
    batch_size = 0
    part_idx = 0
    max_size = max_size_mb * 1024 * 1024

    for f in files:
        if batch_size + f.file_size > max_size and batch:
            out_name = os.path.join(out_dir, f"zdjecia_part{part_idx:03d}.zip")
            with zipfile.ZipFile(out_name, 'w') as zout:
                with zipfile.ZipFile(zip_path, 'r') as zin:
                    for bf in batch:
                        zout.writestr(bf.filename, zin.read(bf.filename))
            print(f"Utworzono: {out_name}")
            part_idx += 1
            batch = []
            batch_size = 0
        batch.append(f)
        batch_size += f.file_size

    # Ostatnia paczka
    if batch:
        out_name = os.path.join(out_dir, f"zdjecia_part{part_idx:03d}.zip")
        with zipfile.ZipFile(out_name, 'w') as zout:
            with zipfile.ZipFile(zip_path, 'r') as zin:
                for bf in batch:
                    zout.writestr(bf.filename, zin.read(bf.filename))
        print(f"Utworzono: {out_name}")

# Najważniejsze: PONIŻSZE URUCHOM! Nie w konsoli, ale jako część pliku Python:

split_zip_by_files('zdjecia.zip', 'output_zip_parts', max_size_mb=200)