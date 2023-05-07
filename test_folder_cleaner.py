from pathlib import Path

from folder_cleaner import sort_file_type, duplicate_cleaner, kill_folders

# define main_dir for file sorting because my folder creating function keeps using the Downloads folder instead of the test_dir
main_dir = Path.home() / "Downloads"

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
    "Videos": ["gifv", "mkv", "mp4"],
}

    
def test_sort_file_type():
    for category, extensions in categories.items():
        for extension in extensions:
            # create a test file
            test_file_name = "test_file." + extension
            test_file_path = Path(main_dir) / test_file_name
            test_file_path.touch()

            # call the function
            sort_file_type(test_file_path)
            
            # check if the file has been moved to the correct directory
            category_folder = Path(main_dir) / category
            assert (category_folder / test_file_name).exists()
            
            # remove the test file and directory if it was created
            (category_folder / test_file_name).unlink()
            if not any(category_folder.iterdir()):
                category_folder.rmdir()


def test_dupliate_cleaner_no_duplicates():
    file_list = [Path(main_dir) / "file1.txt", Path(main_dir) / "file2.txt", Path(main_dir) / "file3.txt"]
    # create test files
    for file in file_list:
        file.touch()

    # call the function
    duplicate_cleaner(list(Path(main_dir).iterdir()))

    # check that all files exist (no dups)
    assert len(list(Path(main_dir).iterdir())) == 3

    # clean up test files
    for file in Path(main_dir).iterdir():
        file.unlink()


def test_duplicate_cleaner_duplicates():
    file_list = [Path(main_dir) / "file1.txt", Path(main_dir) / "file1 (1).txt", Path(main_dir) / "file2.txt", Path(main_dir) / "file2 (4).txt"]
    # create test files
    for file in file_list:
        file.touch()

    # call the function
    duplicate_cleaner(list(Path(main_dir).iterdir()))

    # check that only duplicates were removed
    assert len(list(Path(main_dir).iterdir())) == 2
    assert not any(f.name in ["file1 (1).txt", "file2 (4).txt"] for f in Path(main_dir).iterdir())

    # clean up test files
    for file in Path(main_dir).iterdir():
        file.unlink()


def test_kill_folders_empty_directory():
    # define test_dir to do tests in (can't use Downloads because of hidden system file "desktop.ini", so using a test folder)
    test_dir = Path(main_dir) / "test_dir"
    test_dir.mkdir(exist_ok=True)

    # make empty folder
    empty_directory = Path(test_dir) / "empty_directory"
    empty_directory.mkdir()

    # call the function
    kill_folders(test_dir)

    # check that all folders deleted
    assert not any(Path(test_dir).iterdir())


def test_kill_folders_directory_with_files():
    # define test_dir to do tests in (can't use Downloads because of hidden system file "desktop.ini", so using a test folder)
    test_dir = Path(main_dir) / "test_dir"
    test_dir.mkdir(exist_ok=True)

    # make folder with files
    directory_with_files = Path(test_dir) / "directory_with_files"
    directory_with_files.mkdir()
    (directory_with_files / "file1.txt").touch()
    (directory_with_files / "file2.txt").touch()

    # call the function
    kill_folders(test_dir)

    # check that folder with files was NOT deleted
    assert len(list(Path(test_dir).iterdir())) == 1

    # clean up test files
    (directory_with_files / "file1.txt").unlink()
    (directory_with_files / "file2.txt").unlink()
    directory_with_files.rmdir()


def test_kill_folders_directory_with_empty_directories():
    # define test_dir to do tests in (can't use Downloads because of hidden system file "desktop.ini", so using a test folder)
    test_dir = Path(main_dir) / "test_dir"
    test_dir.mkdir(exist_ok=True)

    # create folder with empty folders inside
    directory_with_empty_directories = Path(test_dir) / "directory_with_empty_directories"
    directory_with_empty_directories.mkdir()
    (directory_with_empty_directories / "empty_directory1").mkdir()
    (directory_with_empty_directories / "empty_directory2").mkdir()

    # call the function
    kill_folders(test_dir)

    # check that all directories were removed
    assert not Path(directory_with_empty_directories).exists()

    # clean up test_dir
    test_dir.rmdir()