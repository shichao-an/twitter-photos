import argparse


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     prog='twphotos')
    parser.add_argument('-u', '--user', help="user account")
    parser.add_argument('-l', '--list',
                        help="list slug with --user as list owner")
