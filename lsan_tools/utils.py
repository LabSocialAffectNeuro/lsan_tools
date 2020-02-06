from glob import glob
import os

__all__ = ['add_file_prefix'
           ]

__author__ = ["Shawn Rhoads"]

def add_file_prefix(files_dir, prefix):
    # adds prefix to every file in specified directory
    assert type(files_dir) == str, "files_dir should be type(str)"
    assert type(prefix) == str, "prefix should be type(str)"

    file_names = glob(os.path.join(files_dir))

    for file in file_names:
        new_filename = os.path.join(os.path.dirname(file),prefix+os.path.basename(file))
        os.rename(file,new_filename)
