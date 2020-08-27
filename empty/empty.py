import os
import argparse
import sys


def try_func(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(e)


def empty_dirs(a_dir, remove=False):
    empty = []
    for root, dirs, files in os.walk(a_dir):
        if len(dirs) == 0 and len(files) == 0:
            empty.append(root)
    if remove:
        for e in empty:
            try_func(os.rmdir, *[e])
    return empty


def main():
    parser = argparse.ArgumentParser(
        prog='empty',
        description='Find and delete empty dirs.')
    parser.add_argument('dir', help='Directory to clean.')
    parser.add_argument('-m', '--max-passes', type=int, default=5,
                        choices=range(1, 6),
                        help='Number of passes to make.')
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        raise FileNotFoundError(args.dir)
    
    for _ in range(args.max_passes):
        _ = empty_dirs(args.dir, remove=True)


if __name__ == '__main__':
    main()
