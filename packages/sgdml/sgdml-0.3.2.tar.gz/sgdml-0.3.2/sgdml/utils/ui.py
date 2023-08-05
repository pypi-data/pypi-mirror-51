from __future__ import print_function

import argparse
import os
import re
import sys

if sys.version[0] == '3':
    raw_input = input

import numpy as np


def yes_or_no(question):
    """
    Ask for yes/no user input on a question.

    Any response besides ``y`` yields a negative answer.

    Parameters
    ----------
        question : :obj:`str`
            User question.
    """

    reply = raw_input(question + ' (y/n): ').lower().strip()
    if not reply or reply[0] != 'y':
        return False
    else:
        return True


def progr_bar(current, total, disp_str='', sec_disp_str=None):
    """
    Print progress bar.

    Example:
    ``[ 45%] Task description (secondary string)``

    Parameters
    ----------
        current : int
            How many items already processed?
        total : int
            Total number of items?
        disp_str : :obj:`str`, optional
            Task description.
        sec_disp_str : :obj:`str`, optional
            Additional string shown in gray.
    """

    is_done = np.isclose(current-total, 0.0)
    progr = float(current) / total

    str_color = pass_str if is_done else info_str
    sys.stdout.write(('\r' + str_color('[%3d%%]') + ' %s') % (progr * 100, disp_str))

    if sec_disp_str is not None:
        sys.stdout.write(' \x1b[90m%s\x1b[0m' % sec_disp_str)

    if is_done:
        sys.stdout.write('\n')

    sys.stdout.flush()


def progr_toggle(is_done, disp_str='', sec_disp_str=None):
    """
    Print progress toggle.

    Example (not done):
    ``[ .. ] Task description (secondary string)``

    Example (done):
    ``[DONE] Task description (secondary string)``

    Parameters
    ----------
        is_done : bool
            Task done?
        disp_str : :obj:`str`, optional
            Task description.
        sec_disp_str : :obj:`str`, optional
            Additional string shown in gray.
    """

    sys.stdout.write(
        '\r%s ' % (pass_str('[DONE]') if is_done else info_str('[') + info_str(blink_str(' .. ')) + info_str(']'))
    )
    sys.stdout.write(disp_str)

    if sec_disp_str is not None:
        sys.stdout.write(' \x1b[90m%s\x1b[0m' % sec_disp_str)

    if is_done:
        sys.stdout.write('\n')

    sys.stdout.flush()


# COLORS

def white_back_str(str):
    return '\x1b[1;7m' + str + '\x1b[0m'


def green_back_str(str):
    return '\x1b[1;30;42m' + str + '\x1b[0m'


def white_bold_str(str):
    return '\x1b[1;37m' + str + '\x1b[0m'


def gray_str(str):
    return '\x1b[90m' + str + '\x1b[0m'


def underline_str(str):
    return '\x1b[4m' + str + '\x1b[0m'


def blink_str(str):
    return '\x1b[5m' + str + '\x1b[0m'


def info_str(str):
    return '\x1b[1;37m' + str + '\x1b[0m'


def pass_str(str):
    return '\x1b[1;32m' + str + '\x1b[0m'


def warn_str(str):
    return '\x1b[1;33m' + str + '\x1b[0m'


def fail_str(str):
    return '\x1b[1;31m' + str + '\x1b[0m'


# USER INPUT VALIDATION


def filter_file_type(dir, type, md5_match=None):

    file_names = []
    for file_name in sorted(os.listdir(dir)):
        if file_name.endswith('.npz'):
            file_path = os.path.join(dir, file_name)
            try:
                file = np.load(file_path, allow_pickle=True)
            except Exception:
                raise argparse.ArgumentTypeError(
                    '{0} contains unreadable .npz files'.format(arg)
                )

            if 'type' in file and file['type'].astype(str) == type[0]:

                # if md5_match is not None:
                #    print(file_name)
                #    print (file['md5'])

                if md5_match is None:
                    file_names.append(file_name)
                elif 'md5' in file and file['md5'] == md5_match:
                    file_names.append(file_name)

            file.close()

    return file_names


def is_file_type(arg, type):
    """
    Validate file path and check if the file is of the specified type.

    Parameters
    ----------
        arg : :obj:`str`
            File path.
        type : {'dataset', 'task', 'model'}
            Possible file types.

    Returns
    -------
        (:obj:`str`, :obj:`dict`)
            Tuple of file path (as provided) and data stored in the
            file. The returned instance of NpzFile class must be
            closed to avoid leaking file descriptors.

    Raises
    ------
        ArgumentTypeError
            If the provided file path does not lead to a NpzFile.
        ArgumentTypeError
            If the file is not readable.
        ArgumentTypeError
            If the file is of wrong type.
        ArgumentTypeError
            If path/fingerprint is provided, but the path is not valid.
        ArgumentTypeError
            If fingerprint could not be resolved.
        ArgumentTypeError
            If multiple files with the same fingerprint exist.

    """

    # Replace MD5 dataset fingerprint with file name, if necessary.
    if type == 'dataset' and not arg.endswith('.npz') and not os.path.isdir(arg):
        dir = '.'
        if re.search(r'^[a-f0-9]{32}$', arg):  # arg looks similar to MD5 hash string
            md5_str = arg
        else:  # is it a path with a MD5 hash at the end?
            md5_str = os.path.basename(os.path.normpath(arg))
            dir = os.path.dirname(os.path.normpath(arg))

            if re.search(r'^[a-f0-9]{32}$', md5_str) and not os.path.isdir(
                dir
            ):  # path has MD5 hash string at the end, but directory is not valid
                raise argparse.ArgumentTypeError('{0} is not a directory'.format(dir))

        file_names = filter_file_type(dir, type, md5_match=md5_str)

        if not len(file_names):
            raise argparse.ArgumentTypeError(
                "No {0} files with fingerprint '{1}' found in '{2}'".format(
                    type, md5_str, dir
                )
            )
        elif len(file_names) > 1:
            error_str = "Multiple {0} files with fingerprint '{1}' found in '{2}'".format(
                type, md5_str, dir
            )
            for file_name in file_names:
                error_str += '\n       {0}'.format(file_name)

            raise argparse.ArgumentTypeError(error_str)
        else:
            arg = os.path.join(dir, file_names[0])

    if not arg.endswith('.npz'):
        argparse.ArgumentTypeError('{0} is not a .npz file'.format(arg))

    try:
        file = np.load(arg, allow_pickle=True)
    except Exception:
        raise argparse.ArgumentTypeError('{0} is not readable'.format(arg))

    if 'type' not in file or file['type'].astype(str) != type[0]:
        raise argparse.ArgumentTypeError('{0} is not a {1} file'.format(arg, type))

    return arg, file


def is_valid_file_type(arg_in):

    arg, file = None, None
    try:
        arg, file = is_file_type(arg_in, 'dataset')
    except argparse.ArgumentTypeError:
        pass

    if file is None:
        try:
            arg, file = is_file_type(arg_in, 'task')
        except argparse.ArgumentTypeError:
            pass

    if file is None:
        try:
            arg, file = is_file_type(arg_in, 'model')
        except argparse.ArgumentTypeError:
            pass

    if file is None:
        raise argparse.ArgumentTypeError(
            '{0} is neither a dataset, task, nor model file'.format(arg)
        )

    return arg, file


# if file is provided, this function acts like its a directory with just one file
def is_dir_with_file_type(arg, type, or_file=False):
    """
    Validate directory path and check if it contains files of the specified type.

    Parameters
    ----------
        arg : :obj:`str`
            File path.
        type : {'dataset', 'task', 'model'}
            Possible file types.
        or_file : bool
            If `arg` contains a file path, act like it's a directory
            with just a single file inside.

    Returns
    -------
        (:obj:`str`, :obj:`list` of :obj:`str`)
            Tuple of directory path (as provided) and a list of
            contained file names of the specified type.

    Raises
    ------
        ArgumentTypeError
            If the provided directory path does not lead to a directory.
        ArgumentTypeError
            If directory contains unreadable files.
        ArgumentTypeError
            If directory contains no files of the specified type.
    """

    if or_file and os.path.isfile(arg):  # arg: file path
        _, file = is_file_type(
            arg, type
        )  # raises exception if there is a problem with file
        file.close()
        file_name = os.path.basename(arg)
        file_dir = os.path.dirname(arg)
        return file_dir, [file_name]
    else:  # arg: dir

        if not os.path.isdir(arg):
            raise argparse.ArgumentTypeError('{0} is not a directory'.format(arg))

        file_names = filter_file_type(arg, type)

        # file_names = []
        # for file_name in sorted(os.listdir(arg)):
        #     if file_name.endswith('.npz'):
        #         file_path = os.path.join(arg, file_name)
        #         try:
        #             file = np.load(file_path)
        #         except Exception:
        #             raise argparse.ArgumentTypeError(
        #                 '{0} contains unreadable .npz files'.format(arg)
        #             )

        #         if 'type' in file and file['type'].astype(str) == type[0]:
        #             file_names.append(file_name)

        #         file.close()

        if not len(file_names):
            raise argparse.ArgumentTypeError(
                '{0} contains no {1} files'.format(arg, type)
            )

        return arg, file_names


def is_strict_pos_int(arg):
    """
    Validate strictly positive integer input.

    Parameters
    ----------
        arg : :obj:`str`
            Integer as string.

    Returns
    -------
        int
            Parsed integer.

    Raises
    ------
        ArgumentTypeError
            If integer is not > 0.
    """
    x = int(arg)
    if x <= 0:
        raise argparse.ArgumentTypeError('must be strictly positive')
    return x


def parse_list_or_range(arg):
    """
    Parses a string that represents either an integer or a range in
    the notation ``<start>:<step>:<stop>``.

    Parameters
    ----------
        arg : :obj:`str`
            Integer or range string.

    Returns
    -------
        int or :obj:`list` of int

    Raises
    ------
        ArgumentTypeError
            If input can neither be interpreted as an integer nor a valid range.
    """

    if re.match(r'^\d+:\d+:\d+$', arg) or re.match(r'^\d+:\d+$', arg):
        rng_params = list(map(int, arg.split(':')))

        step = 1
        if len(rng_params) == 2:  # start, stop
            start, stop = rng_params
        else:  # start, step, stop
            start, step, stop = rng_params

        rng = list(range(start, stop + 1, step))  # include last stop-element in range
        if len(rng) == 0:
            raise argparse.ArgumentTypeError('{0} is an empty range'.format(arg))

        return rng
    elif re.match(r'^\d+$', arg):
        return int(arg)

    raise argparse.ArgumentTypeError(
        '{0} is neither a integer list, nor valid range in the form <start>:[<step>:]<stop>'.format(
            arg
        )
    )


def is_task_dir_resumeable(
    train_dir, train_dataset, test_dataset, n_train, n_test, sigs, gdml
):
    r"""
    Check if a directory contains `task` and/or `model` files that
    match the configuration of a training process specified in the
    remaining arguments.

    Check if the training and test datasets in each task match
    `train_dataset` and `test_dataset`, if the number of training and
    test points matches and if the choices for the kernel
    hyper-parameter :math:`\sigma` are contained in the list. Check
    also, if the existing tasks/models contain symmetries and if
    that's consistent with the flag `gdml`. This function is useful
    for determining if a training process can be resumed using the
    existing files or not.

    Parameters
    ----------
        train_dir : :obj:`str`
            Path to training directory.
        train_dataset : :obj:`dataset`
            Dataset from which training points are sampled.
        test_dataset : :obj:`test_dataset`
            Dataset from which test points are sampled (may be the
            same as `train_dataset`).
        n_train : int
            Number of training points to sample.
        n_test : int
            Number of test points to sample.
        sigs : :obj:`list` of int
            List of :math:`\sigma` kernel hyper-parameter choices
            (usually: the hyper-parameter search grid)
        gdml : bool
            If `True`, don't include any symmetries in model (GDML),
            otherwise do (sGDML).

    Returns
    -------
        bool
            False, if any of the files in the directory do not match
            the training configuration.
    """

    for file_name in sorted(os.listdir(train_dir)):
        if file_name.endswith('.npz'):
            file_path = os.path.join(train_dir, file_name)
            file = np.load(file_path, allow_pickle=True)

            if 'type' not in file:
                continue
            elif file['type'] == 't' or file['type'] == 'm':

                if (
                    file['md5_train'] != train_dataset['md5']
                    or file['md5_valid'] != test_dataset['md5']
                    or len(file['idxs_train']) != n_train
                    or len(file['idxs_valid']) != n_test
                    or gdml
                    and file['perms'].shape[0] > 1
                    or file['sig'] not in sigs
                ):
                    return False

    return True


def is_lattice_supported(lat):

    is_supported = False
    if (
        np.all(lat == np.diag(np.diagonal(lat)))
        and len(set(np.diag(lat)))  # diagonal matrix?
        == 1  # all diagonal elements all the same?
    ):
        is_supported = True

    return is_supported
