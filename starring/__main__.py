import sys
import argparse

try:
    from core import *
except ImportError as exception:
    sys.exit(f"Some program module not found: {exception}")


def parse_arg():
    """Парсер аргументов"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="user for whom me will receive information", required=True)
    return parser.parse_args()


def main():
    """Точка входа"""
    try:
        args = parse_arg()
        worker = Worker(args.user)
        starred_rep = worker.get_starring_rep()
        worker.print_info(starred_rep)
    except Exception as e:
        print("Error: {}".format(e))


if __name__ == '__main__':
    main()
