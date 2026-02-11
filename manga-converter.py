import os
import zipfile
from tqdm import tqdm

'''
This script converts .zip files downloaded from mangakatana.com into
ONE .cbz volume per zip file.

Each .zip contains multiple chapter folders like:
c001, c002, c003, ...

Each chapter folder contains images named:
001.jpg, 002.jpg, 003.jpg, ...

The script merges all chapters into one CBZ while preserving order.
The output CBZ keeps the same name as the ZIP file.
A progress bar shows extraction progress.
'''

def main():
    whereiam = os.path.dirname(os.path.abspath(__file__))
    root_folder = whereiam

    cbz_folder = os.path.join(root_folder, "cbz")
    if not os.path.exists(cbz_folder):
        os.makedirs(cbz_folder)

    for zip_file in os.listdir(root_folder):
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(root_folder, zip_file)

            base_name = os.path.splitext(zip_file)[0]
            cbz_path = os.path.join(cbz_folder, f"{base_name}.cbz")

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    folders = sorted([
                        name for name in zip_ref.namelist()
                        if name.endswith("/") and name.startswith("c")
                    ])

                    # get all images in order
                    ordered_files = []
                    for folder in folders:
                        files = sorted([
                            f for f in zip_ref.namelist()
                            if f.startswith(folder) and not f.endswith("/")
                        ])
                        ordered_files.extend(files)

                    with zipfile.ZipFile(cbz_path, 'w', compression=zipfile.ZIP_DEFLATED) as cbz:
                        for file in tqdm(ordered_files, desc=f"Processing {zip_file}", unit="img"):
                            file_content = zip_ref.read(file)

                            folder = os.path.dirname(file)
                            chapter_number = folder[1:]  # remove 'c' → "001"

                            index = ordered_files.index(file)
                            ext = os.path.splitext(file)[1]

                            new_name = f"{chapter_number}_{index:05d}{ext}"
                            cbz.writestr(new_name, file_content)

                print(f"Finished: {zip_file} → {base_name}.cbz")

            except Exception as e:
                print(f"Error processing ZIP: {zip_path}\n{e}")

    print("Done!")

if __name__ == "__main__":
    main()
