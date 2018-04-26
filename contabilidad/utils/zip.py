import os
import zipfile


def unzip(zip_path, working_path):
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    zip_ref.extractall(working_path)
    zip_ref.close()


def get_files(path):
    if os.path.exists(path):
        return os.listdir(path)
    return []


def get_folder_name(path):
    exclude = ['__MACOSX']
    file_name = ""
    if os.path.exists(path):
        folders = [name for name in os.listdir(path) if name not in exclude]
        file_name = folders[0] if len(folders) > 0 else ""
    return "{}/{}".format(path, file_name)
