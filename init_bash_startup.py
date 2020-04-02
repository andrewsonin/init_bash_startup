#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from os.path import exists
from pathlib import Path
from typing import Union

TEMPLATE_DIR = 'templates'


def parse_args() -> Namespace:
    """
    Parses arguments the from command line and makes them global variables.

    Returns:
        The resulting parsing namespace
    """
    parser = ArgumentParser(description='.bashrc and .bash_profile initialization script.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--macos',
        dest='is_macos',
        action='store_true',
        default=False,
        help='specify this argument if the OS is macOS'
    )
    group.add_argument(
        '--linux',
        dest='is_macos',
        action='store_false',
        help='specify this argument if the OS is Linux'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--append_to_bashrc',
        dest='append_to_bashrc',
        action='store_true',
        default=False,
        help='specify this argument if you just want to append information to the .bashrc file instead of rewriting'
    )
    group.add_argument(
        '--rewrite_bashrc',
        dest='rewrite_bashrc',
        action='store_true',
        default=False,
        help='specify this argument if you want to rewrite the .bashrc file'
    )
    group.add_argument(
        '--no_bashrc',
        dest='use_bashrc',
        action='store_false',
        default=True,
        help='specify this argument if you do not want to deal with the .bashrc file'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--append_to_bash_profile',
        dest='append_to_bash_profile',
        action='store_true',
        default=False,
        help='specify this argument if you just want to append information to the .bash_profile file '
             'instead of rewriting'
    )
    group.add_argument(
        '--rewrite_bash_profile',
        dest='rewrite_bash_profile',
        action='store_true',
        default=False,
        help='specify this argument if you want to rewrite the .bash_profile file'
    )
    group.add_argument(
        '--no_bash_profile',
        dest='use_bash_profile',
        action='store_false',
        default=True,
        help='specify this argument if you do not want to deal with the .bash_profile file'
    )
    return parser.parse_args()


def ensure_file_not_exists(path_to_file: Union[str, Path]) -> None:
    """
    Checks if the file of interest does not exist.

    Args:
        path_to_file:     Path to the file of interest
    Raises:
        FileExistsError:  In the case if the file exists

    Returns:
        None
    """
    if exists(path_to_file):
        raise FileExistsError(
            f'File {path_to_file} exists. Try to specify an append mode or just delete it'
        )


def init_bashrc(path_to_bashrc: Union[str, Path], macos: bool, append: bool) -> None:
    """
    Initializes .bashrc file.

    Args:
        path_to_bashrc:  Path to a .bashrc file
        macos:           Indicates that the OS is macOS
        append:          Indicates that the file will be opened in append mode instead of write mode

    Returns:
        None
    """
    path_to_templates = Path(__file__).parent / TEMPLATE_DIR
    with open(path_to_templates / 'common_bashrc_template.bash', 'r') as common_bashrc_template:
        content = common_bashrc_template.read()
    if macos:
        with open(path_to_templates / 'macos_bashrc_additions.bash', 'r') as macos_bashrc_additions:
            content = macos_bashrc_additions.read() + content

    with open(path_to_bashrc, 'a' if append else 'w') as bashrc:
        bashrc.write(content)


def init_bash_profile(path_to_bash_profile: Union[str, Path], append: bool) -> None:
    """
    Initializes .bash_profile file.

    Args:
        path_to_bash_profile:  Path to a .bash_profile file
        append:                Indicates that the file will be opened in append mode instead of write mode

    Returns:
        None
    """
    with open(path_to_bash_profile, 'a' if append else 'w') as bash_profile:
        bash_profile.write('. ~/.bashrc\n')


if __name__ == '__main__':
    args = parse_args()

    home_dir = Path.home()
    bashrc = home_dir / '.bashrc'
    bash_profile = home_dir / '.bash_profile'

    if args.use_bashrc and not (args.append_to_bashrc or args.rewrite_bashrc):
        ensure_file_not_exists(bashrc)
    if args.use_bash_profile and not (args.append_to_bash_profile or args.rewrite_bash_profile):
        ensure_file_not_exists(bash_profile)

    if args.use_bashrc:
        init_bashrc(
            bashrc,
            args.is_macos,
            args.append_to_bashrc
        )
    if args.use_bash_profile:
        init_bash_profile(
            bash_profile,
            args.append_to_bash_profile
        )

else:
    raise ImportError(f'File {__file__} cannot be imported')
