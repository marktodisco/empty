import os
import argparse
import sys
import logging
from functools import partial

from tqdm import trange

trange = partial(trange, ncols=80)
logging.basicConfig(
    filename='debug.log',
    style='{',
    level=logging.DEBUG,
    format='{asctime} - empty - {funcName} - {levelname} - {message}',
    datefmt='%Y-%m-%d %I:%M:%S %p')


def try_func(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        logging.error(e)


def empty_dirs(a_dir, remove=False):
    empty = []
    for root, dirs, files in os.walk(a_dir):
        if len(dirs) == 0 and len(files) == 0:
            empty.append(root)
    if remove:
        for e in empty:
            try_func(os.rmdir, *[e])
    return empty


def dry_run(args):
    mapping = {}
    mapping.update(vars(args))
    path = os.path.abspath(args.path)
    msg = (
        '\nPositional Arguments\n'
        '--------------------\n'
        '  path: {path}\n'
        '\n'
        'Optional Arguments\n'
        '------------------\n'
        '  --max-passes: {max_passes}\n'
        '\n'
    )
    print(msg.format(**mapping))
    logging.info(f'Dry-run excuted for {path}.')


def main():
    parser = argparse.ArgumentParser(
        prog='empty',
        description='Find and delete empty dirs.')
    parser.add_argument('path', help='Directory to clean.')
    parser.add_argument('-m', '--max-passes', type=int, default=1,
                        help='Number of passes to make. Default is 1.')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='Print arguments for testing.')
    args = parser.parse_args()
    
    if args.dry_run:
        dry_run(args)
        return
    
    path = os.path.abspath(args.path)
    if not os.path.exists(path):
        logging.error(f'Directory not found: {path}')
        logging.info('Quitting program.')
        raise FileNotFoundError(path)
    
    logging.info(f'Starting analysis on {path}')
    empty_counter = 0
    for _ in trange(args.max_passes):
        empty = empty_dirs(path, remove=True)
        empty_counter += len(empty)
    logging.info(f'Removed {empty_counter} empty folders.')
    logging.info(f'Analysis of {path} ended cleanly.')


if __name__ == '__main__':
    main()
