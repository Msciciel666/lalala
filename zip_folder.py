import os
import zipfile

# Ścieżka do folderu, który chcesz spakować (zmień na swój!)
folder_to_zip = r"C:\xampp\htdocs\darkweb666"

# Gdzie utworzyć ZIP? (tu: obok folderu)
output_zip = os.path.join(os.path.dirname(folder_to_zip), os.path.basename(folder_to_zip) + ".zip")

def zipdir(path, ziph):
    # Dodaje cały folder do zipa
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            # Relatywna ścieżka w ZIP (bez pełnej ścieżki z dysku)
            arcname = os.path.relpath(full_path, os.path.dirname(path))
            ziph.write(full_path, arcname)

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(folder_to_zip, zipf)

print(f"Spakowano do: {output_zip}")
