#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © %YEAR% %USER% <%MAIL%>
#
# Distributed under terms of the %LICENSE% license.

"""
%HERE%
"""

from loguru import logger

# logger = logging.getLogger()
import argparse
import os
import os.path as op
import stat
from io3d.network import download_file

def rm_smart(filename):
    filename = op.expanduser(filename)
    if op.exists(filename):
        os.remove(filename)


def create_lisa_data_dir_tree(oseg=None):

    odp = op.expanduser('~/lisa_data/.lisa/')
    if not op.exists(odp):
        os.makedirs(odp)

    # import wget
    lisa_icon_path= path(".lisa/LISA256.png")
    if not op.exists(lisa_icon_path):
        try:
            download_file(
                "https://raw.githubusercontent.com/mjirik/lisa/master/lisa/icons/LISA256.png",
                filename=lisa_icon_path)
            # wget.download(
            #     "https://raw.githubusercontent.com/mjirik/lisa/master/lisa/icons/LISA256.png",
            #     out=lisa_icon_path)
        except:
            import traceback
            logger.warning('logo download failed')
            logger.warning(traceback.format_exc())

    if oseg is not None:
        # used for server sync
        oseg._output_datapath_from_server = op.join(oseg.output_datapath, 'sync', oseg.sftp_username, "from_server/")
        # used for server sync
        oseg._output_datapath_to_server = op.join(oseg.output_datapath, 'sync', oseg.sftp_username, "to_server/")
        odp = oseg.output_datapath
        if not op.exists(odp):
            os.makedirs(odp)
        odp = oseg._output_datapath_from_server
        if not op.exists(odp):
            os.makedirs(odp)
        odp = oseg._output_datapath_to_server
        if not op.exists(odp):
            os.makedirs(odp)



def make_icon():
    import platform

    system = platform.system()
    if system == 'Darwin':
        # MacOS
        create_lisa_data_dir_tree()
        __make_icon_osx()
        pass
    elif system == "Linux":
        create_lisa_data_dir_tree()
        __make_icon_linux()

def path(*path_suffix):
    """
    :path_suffix: relative path in lisa_data dir, may be an array
    :return: directory with lisa data
    """
    lpath = op.expanduser('~/lisa_data')
    if len(path_suffix) > 0:
        lpath = op.join(lpath, *path_suffix)
    return lpath

def get_conda_path():
    import os.path as op
    conda_path_candidates = [
        "~/anaconda/bin",
        "~/miniconda/bin",
        "~/anaconda2/bin",
        "~/miniconda2/bin",
    ]
    for cpth in conda_path_candidates:
        conda_pth = op.expanduser(cpth)
        if op.exists(conda_pth):
            return conda_pth
    return None

def file_copy_and_replace_lines(in_path, out_path):
    """
    Used for
    :param in_path:
    :param out_path:
    :return:
    """
    import shutil
    import fileinput

    # print "path to script:"
    # print path_to_script
    # lisa_path = os.path.abspath(path_to_script)
    #
    shutil.copy2(in_path, out_path)
    # conda_path = get_conda_path()

    # print 'ip ', in_path
    # print 'op ', out_path
    # print 'cp ', conda_path
    for line in fileinput.input(out_path, inplace=True):
        # coma on end makes no linebreak
        # line = line.replace("@{LISA_PATH}", lisa_path)
        line = replace_tags(line)
        print(line)

def replace_tags(text):
    conda_path = get_conda_path()
    text = text.replace("@{CONDA_PATH}", conda_path)
    text = text.replace("@{LISA_DATA_PATH}", path())
    return text

def __make_icon_osx():
    lisa_shortcut = op.expanduser("~/Desktop/lisa")
    if not os.path.exists(lisa_shortcut):
        with open(lisa_shortcut, 'w') as outfile:
            outfile.write(
            "\
#!/bin/bash\n\
export PATH=$HOME/miniconda2/bin:$HOME/anaconda2/bin:$HOME/miniconda/bin:$HOME/anaconda/bin:$PATH\n\
lisa"
            )
        os.chmod(lisa_shortcut,
                 stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH |
                 stat.S_IRUSR | stat.S_IRGRP | stat.S_IXOTH |
                 stat.S_IWUSR | stat.S_IWGRP
                 )

    lisa_icon_path= op.expanduser("~/lisa_data/.lisa/LISA256.icns")
    if not os.path.exists(lisa_icon_path):
        try:
            download_file(
            # wget.download(
                "https://raw.githubusercontent.com/mjirik/lisa/master/applications/LISA256.icns",
                filename=lisa_icon_path
                # out=lisa_icon_path
            )

        except:
            logger.warning('logo download failed')
            pass
    # import wget
    # wget.download(
    #     "https://raw.githubusercontent.com/mjirik/lisa/master/lisa/requirements_pip.txt",
    #     out=lidapath() + "lisa_gui"
    # )
    # home_path = os.path.expanduser('~')
    # in_path = os.path.join(path_to_script, "applications/lisa_gui")
    # dt_path = os.path.join(home_path, "Desktop")
    # subprocess.call(['ln', '-s', in_path, dt_path])

def __make_icon_linux():
    # import wget
    in_path = op.expanduser("~/lisa_data/.lisa/lisa.desktop.in")
    rm_smart(in_path)
    lisa_icon_path= op.expanduser("~/lisa_data/.lisa/LISA256.png")
    # if not op.exists(in_path):
    #     try:
    #         wget.download(
    #             "https://raw.githubusercontent.com/mjirik/lisa/master/applications/lisa.desktop.in",
    #             out=in_path)
    #     except:
    #         import traceback
    #         logger.warning('logo download failed')
    #         logger.warning(traceback.format_exc())
    if not op.exists(lisa_icon_path):
        try:
            download_file(
            # wget.download(
                "https://raw.githubusercontent.com/mjirik/lisa/master/lisa/icons/LISA256.png",
                filename=lisa_icon_path)
            # out=lisa_icon_path)
        except:
            import traceback
            logger.warning('logo download failed')
            logger.warning(traceback.format_exc())

    logger.debug("icon input path:")
    logger.debug(in_path)

    home_path = os.path.expanduser('~')

    if os.path.exists(os.path.join(home_path, 'Desktop')):
        desktop_path = os.path.join(home_path, 'Desktop')
    elif os.path.exists(os.path.join(home_path, 'Plocha')):
        desktop_path = os.path.join(home_path, 'Plocha')
    else:
        print("Cannot find desktop directory")
        logger.error("Cannot find desktop directory")
        desktop_path = None

    # copy desktop files to desktop
    if desktop_path is not None:
        out_path = os.path.join(desktop_path, "lisa.desktop")
        __make_linux_icon_file(out_path)

    # copy desktop files to $HOME/.local/share/applications/
    # to be accesable in application menu (Linux)
    local_app_path = os.path.join(home_path, '.local/share/applications')
    if os.path.exists(local_app_path) and os.path.isdir(local_app_path):
        out_path = os.path.join(local_app_path, "lisa.desktop")
        __make_linux_icon_file(out_path)
    else:
        print("Couldnt find $HOME/.local/share/applications/.")

def __make_linux_icon_file(lisa_shortcut):
    if not os.path.exists(lisa_shortcut):
        file_content = "\
[Desktop Entry]\n\
Name=LISA\n\
GenericName=LISA\n\
Comment=LIver Surgery Analyser\n\
Exec=bash -c 'export PATH=@{CONDA_PATH}:$PATH ; lisa'\n\
Terminal=false\n\
Type=Application\n\
Icon=@{LISA_DATA_PATH}/.lisa/LISA256.png\n\
Categories=Application;Science;MedicalSoftware;\n\
StartupNotify=false\n"
        file_content = replace_tags(file_content)
        with open(lisa_shortcut, 'w') as outfile:
            outfile.write(file_content)
        os.chmod(lisa_shortcut,
                 stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH |
                 stat.S_IRUSR | stat.S_IRGRP | stat.S_IXOTH |
                 stat.S_IWUSR | stat.S_IWGRP
                 )
    # fi = fileinput.input(out_path, inplace=True)
    print("icon output path: \n", lisa_shortcut)


def main():
    # logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('log.txt')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.debug('start')

    # input parser
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        # required=True,
        help='input file'
    )
    parser.add_argument(
        '-icn', '--icon',
        default=False,
        action='store_true',
        # required=True,
        help='make icon'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)

    if args.icon:
        make_icon()


if __name__ == "__main__":
    main()