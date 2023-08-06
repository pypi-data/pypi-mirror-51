#
#                __   _,--="=--,_   __
#               /  \."    .-.    "./  \
#              /  ,/  _   : :   _  \/` \
#              \  `| /o\  :_:  /o\ |\__/
#               `-'| :="~` _ `~"=: |
#                  \`     (_)     `/
#           .-"-.   \      |      /   .-"-.
#    .-----{     }--|  /,.-'-.,\  |--{     }-----.
#     )    (_)_)_)  \_/`~-===-~`\_/  (_(_(_)    (
#    (                                           )
#     )                Oriole-CLI               (
#    (                  Eric.Zhou                )
#    '-------------------------------------------'
#

import argparse


def _add_parser(parser, module, name):
    module_parser = parser.add_parser(name)
    module.init_parser(module_parser)
    module_parser.set_defaults(main=module.main)


def add_parser(parser, modules):
    for module in modules:
        name = module.__name__.split('.')[-1]
        _add_parser(parser, module, name[0])


def exec_cli(modules):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_parser(subparsers, modules)
    args = parser.parse_args()
    return args.main(args)
