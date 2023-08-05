import fnmatch
import os
import shutil
import subprocess
from itertools import zip_longest
from subprocess import PIPE, CalledProcessError, Popen
from time import sleep
from warnings import warn

from tqdm.auto import tqdm

from . import config


class StorageResource(object):
    """ Defines a storage resource object"""

    def __init__(self, urlpath, loc_type, exclude_patterns, file_extension='.nc', fs=None):
        """

        Parameters
        -----------

        urlpath : str
              Path to storage resource
        loc_type : str
              Type of storage resource. Supported resources include: posix, hsi (tape)
        exclude_patterns : str, list
               Directories to exclude during catalog generation
        file_extension : str, default `.nc`
              File extension

        """

        self.fs = fs
        self.urlpath = urlpath
        self.type = loc_type
        self.file_extension = file_extension
        self.exclude_patterns = exclude_patterns
        self.filelist = self._list_files()

    def _list_files(self):
        """ Get file listing for different location types such as
            tapes, posix filesystem, filelist.
        """

        if self.type == 'posix':
            filelist = self._list_files_posix()

        elif self.type == 'hsi':
            filelist = self._list_files_hsi()

        elif self.type == 'input-file':
            filelist = self._list_files_input_file()

        elif self.type == 'copy-to-cache':
            filelist = self._list_files_posix()

        elif self.type == 'aws-s3':
            filelist = self._list_s3_objects()

        else:
            raise ValueError(f'unknown resource type: {self.type}')

        return list(filter(self._filter_func, filelist))

    def _filter_func(self, path):
        return not any(
            fnmatch.fnmatch(path, pat=exclude_pattern) for exclude_pattern in self.exclude_patterns
        )

    def _list_s3_objects(self):
        """ Get a list of s3 objects.

        Notes
        -----
        The following implementation uses
        s3fs: https://github.com/dask/s3fs for S3 Filesystem.
        """
        if self.fs:
            try:
                objects = self.fs.ls(self.urlpath)[1:]
                objects = [obj for obj in objects if obj.endswith(self.file_extension)]
                return objects
            except Exception as exc:
                raise exc
        else:
            raise ValueError(
                'Please authenticate with s3fs, and make sure to call\n'
                'StorageResource() with `fs` set to your authentication object.'
            )

    def _list_files_posix(self):
        """Get a list of files"""
        try:

            w = os.walk(self.urlpath, followlinks=True)

            filelist = []

            for root, dirs, files in w:
                filelist.extend(
                    [os.path.join(root, f) for f in files if f.endswith(self.file_extension)]
                )
            return filelist
        except Exception as e:
            warn(
                f'{e.__str__()}\nCould not parse content in directory = {self.urlpath}. Skipping directory.'
            )
            return []

    def _list_files_hsi(self):
        """Get a list of files from HPSS tapes"""
        if shutil.which('hsi') is None:
            warn(f'no hsi; cannot access [HSI]{self.urlpath}')
            return []

        p = subprocess.Popen(
            [
                'hsi',
                'find {urlpath} -name "*{file_extension}"'.format(
                    urlpath=self.urlpath, file_extension=self.file_extension
                ),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        filelist = []
        skip = True
        while p.poll() is None:
            line = p.stderr.readline().decode('UTF-8').strip()
            if skip:
                skip = False
            elif '***' in line:
                skip = True
            elif not line:
                break
            else:
                filelist.append(line)

        return filelist

    def _list_files_input_file(self):
        """return a list of files from a file containing a list of files"""
        with open(self.urlpath, 'r') as fid:
            return fid.read().splitlines()


def _transfer_files(processes):

    """Executes a list of child programs in new processes"""

    errored = []
    completed = []
    while processes:
        for p in processes:
            if p.poll() is not None:
                if p.returncode != 0:
                    errored.append(p)
                else:
                    completed.append(p)
                processes.remove(p)

    for p in completed:
        stdout, stderr = p.communicate()
        print('-' * 80)
        print('completed')
        print(p.args)
        print(stdout.decode('UTF-8'))
        print(stderr.decode('UTF-8'))
        print()

    if errored:
        for p in errored:
            stdout, stderr = p.communicate()
            print('-' * 80)
            print('ERROR!')
            print(p.args)
            print(stdout.decode('UTF-8'))
            print(stderr.decode('UTF-8'))
            print()
        raise CalledProcessError(errored[0].returncode, errored[0].args)


def _posix_symlink(file_remote_local):
    """Create symlinks of posix files into data-cache-directory.

    Parameters
    ----------
    file_remote_local : list of tuples
        List of the form: [(file_remote, file_local), ...]

    """
    cmds = [['ln', '-s', file_remote, file_local] for file_remote, file_local in file_remote_local]
    processes = [Popen(cmd, stderr=PIPE, stdout=PIPE) for cmd in cmds]

    _transfer_files(processes)


def _get_hsi_files(file_remote_local):
    """Transfer files from HPSS.

    Parameters
    ----------
    file_remote_local : list of tuples
        List of the form: [(file_remote, file_local), ...]

    """

    hsi_max_concurrent = 5
    args = [iter(file_remote_local)] * hsi_max_concurrent

    for groups in tqdm(
        list(zip_longest(*args, fillvalue=None), disable=not config.get('progress-bar'))
    ):

        cmds = [
            ['hsi', f'cget {file_rem_loc[1]} : {file_rem_loc[0]}']
            for file_rem_loc in groups
            if file_rem_loc is not None
        ]

        processes = [Popen(cmd, stderr=PIPE, stdout=PIPE) for cmd in cmds]

        _transfer_files(processes)
