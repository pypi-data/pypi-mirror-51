#!/usr/bin/env python3

import argparse
from init import init as init_handler
from update import update as update_handler
from generate import generate as generate_handler


def main():
    parser = argparse.ArgumentParser(prog='vup', description='Version updater')
    sub = parser.add_subparsers()

    gen = sub.add_parser('generate', help='generate version file')
    gen.set_defaults(handler=generate_handler)
    gen.add_argument('--language', '-x', choices=('c++', 'c'), help='output language (default: c++)', default='c++')
    gen.add_argument('--output', '-o', help='output file base name (default: vup)', default='vup')
    gen.add_argument('--pre-update', '--pre', action='store_true', help='update before generate')
    gen.add_argument('--post-update', '--post', action='store_true', help='update after generate')
    gen.add_argument(
        '--standard', '--std',
        choices=('c++03', 'c++11', 'c++14', 'c++17'),
        help='C++ standard version (default: c++11)',
        default='c++11')

    update = sub.add_parser('update', help='update current version')
    update.set_defaults(handler=update_handler)
    [
        update.add_argument(
            '--{}'.format(t),
            action='store_true',
            help='update {0} version if {0} type is manual'.format(t))
        for t in ('major', 'minor', 'build', 'revision')
    ]

    init = sub.add_parser('init', help='initialize configuration file')
    init.set_defaults(handler=init_handler)
    # init.add_argument('--interactive', '-i', action='store_true', help='run init as interactive mode')
    for p in ('major', 'minor', 'build', 'revision'):
        init.add_argument(
            '--{}-type'.format(p),
            choices=('auto', 'manual', 'year', 'month', 'day', 'days', 'none'),
            help='{} version style (auto: auto increment, '
                 'manual: increment by command execute, '
                 'days: number of days from specific date, '
                 'none: not use this field'.format(p),
            required=True)
        init.add_argument(
            '--{}'.format(p),
            help='initial value for {}'.format(p))
        init.add_argument(
            '--{}-from'.format(p),
            help='days: from date(YYYY-MM-DD)',
            default=None,
        )

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.parse_args()


if __name__ == '__main__':
    main()
