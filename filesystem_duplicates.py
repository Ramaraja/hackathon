"""
Given a folder, walk through all files within the folder and subfolders
and get list of all files that are duplicates
The md5 checcksum for each file will determine the duplicates
"""

import os
import hashlib
import json
from collections import defaultdict, Counter


def generate_md5(fname, chunk_size=1024):
    """
    Function which takes a file name and returns md5 checksum of the file
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        # Read the 1st block of the file
        chunk = f.read(chunk_size)
        # Keep reading the file until the end and update hash
        while chunk:
            hash.update(chunk)
            chunk = f.read(chunk_size)

    # Return the hex checksum
    return hash.hexdigest()


def check_duplicate_files(workspace, ccid, search_dirs=None):
    """
    Starting block of script
    """
    workspace_dir = workspace + ccid
    # The dict will have a list as values
    md5_dict = defaultdict(list)

    if search_dirs is None:
        search_dirs = ['audio', 'businessobjects', 'grammars', 'messages']

    # Below code is used for file extension based search
    # file_types_inscope = ["ppt", "pptx", "pdf", "txt", "html",
    #                       "mp4", "jpg", "png", "mp3",
    #                       "vox", "wav", 'grxml', 'json']

    # Walk through all files and folders within directory
    for path, dirs, files in os.walk(workspace_dir):
        defpath = path.split('/')[4:5]
        res = any(elem in defpath for elem in search_dirs)
        if res:
            for each_file in files:
                # if each_file.split(".")[-1].lower() in file_types_inscope:
                    # The path variable gets updated for each subfolder
                    file_path = os.path.join(path, each_file)
                    # If there are more files with same checksum append to list
                    md5_dict[generate_md5(file_path)].append(file_path)

    # Identify keys (checksum) having more than one values (file names)
    duplicate_files = (val for key, val in md5_dict.items() if len(val) > 1)
    file_list = []
    file_dict = defaultdict(list)
    dir_paths = ''
    for file_ls in duplicate_files:
        for path in file_ls:
            top_level_path = path.split('/')[:5]
            dir_paths = '/'.join(top_level_path)
        file_dict[dir_paths].append(file_ls)
        file_list.append(dir_paths)
    dup_file_dir_count = dict(Counter(file_list))
    dup_file_dir_count_json = json.dumps([dup_file_dir_count])
    file_dict_json = json.dumps([file_dict])
    return dup_file_dir_count_json, file_dict_json

# if __name__== "__main__":
#   check_duplicate_files('../ofs/', '00b392fd-c977-4be5-bf20-54c43a3a2a13')
