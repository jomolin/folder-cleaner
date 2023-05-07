import re
import send2trash as s2t

from pathlib import Path


# directory to be monitored
directory = Path.home() / "Downloads"

# dictionary of file categories and extensions to look for
categories = {
    "Archives": ["7z", "rar", "zip"],
    "Books": ["epub"],
    "DataFiles": ["csv", "db", "json", "xls", "xlsx"],
    "Discs": ["iso"],
    "Docs": ["doc", "docx", "hwp", "md", "txt"],
    "Installers": ["dmg", "exe", "msi"],
    "Images": ["bmp", "gif", "jpg", "jpeg", "png", "svg"],
    "Music": ["aac", "flac", "mp3", "ogg", "wav"],
    "PDFs": ["pdf"],
    "Subtitles": ["smi", "srt"],
    "Torrents": ["torrent"],
    "Videos": ["gifv", "mkv", "mp4", "webm"],
}


def main():
    # get list of existing files in directory
    existing_files = list(Path(directory).iterdir())

    # First! check for duplicate files and move them to bin
    duplicate_cleaner(existing_files)

    # Second! categorize and move existing files into named directories
    for filename in existing_files:
        sort_file_type(filename)

    # Third! remove any empty folders
    kill_folders(directory)

    # Print end! SUCCESS!
    print("SUCCESS! Enjoy your clean folder.")


def duplicate_cleaner(existing_files):
    # create dictionary to store file sizes(keys) and file names(values)
    file_sizes = {}

    # Loop through each file in directory
    for file_path in directory.glob("*"):
        # if not a directory get it's size
        # I ran into a problem where desktop.ini kept causing the program to crash on my system, so I added an exception
        if file_path.is_file() and file_path.name != "desktop.ini":
            file_size = file_path.stat().st_size

            # if this size doesn't exist yet, add it to dictionary with empty list
            if file_size not in file_sizes:
                file_sizes[file_size] = []

            # then add the file name into the list for this file size
            file_sizes[file_size].append(file_path)

    # Loop through filled dictionary
    for file_size in file_sizes:
        # If multiple files with same size
        if len(file_sizes[file_size]) > 1:
            # check each file name in that size
            for file_path in file_sizes[file_size]:
                # file name contains file_name (number).ext
                match = re.match(r"^(.+?)\s\(\d+\)(\.\w+)$", file_path.name)

                # if file name is duplicated
                if match:
                    # get base file name
                    base_name = match.group(1).lower()
                    # get file extension
                    extension = match.group(2).lower()

                    # check if base_name is in list with matching extension
                    for f in file_sizes[file_size]:
                        if (base_name + extension) == f.name.lower() and f != file_path:
                            # move to bin
                            try:
                                s2t.send2trash(file_path)
                                existing_files.remove(file_path)
                                print(f"Moved duplicate file {file_path.name} to bin.")
                            except:
                                print(f"Could not move {file_path.name} to bin. Skipping...")
                            break


def kill_folders(directory):
    # recursively search for empty folders and remove them
    for subdir in directory.iterdir():
        if subdir.is_dir():
            kill_folders(subdir)    # recursively call kill folders
            if not any(subdir.iterdir()):
                print(f"Removing empty folder: {subdir}")
                subdir.rmdir()  # remove directory if empty


def sort_file_type(filename):
    file_path = Path(filename)
    # find file extension
    extension = file_path.suffix.lower()[1:]

    # iterate over categories
    for category, extensions in categories.items():
        # move file if it matches an extension in the dictionary
        if extension.lower() in extensions:
            # create folder if it doesn't exist
            category_folder = directory / category
            category_folder.mkdir(exist_ok=True)
            # create file path
            source_path = file_path.resolve()
            destination_path = category_folder / file_path.name

            try:
                # finally move the file
                source_path.rename(destination_path)
                print(f"Moved {filename} to {category}")
                break
            except:
                print(f"Error encountered while moving {filename}. Skipping...")
                break


if __name__ == "__main__":
    main()
