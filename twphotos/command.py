import argparse


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     prog='twphotos')
    parser.add_argument('-u', '--user',
                        help="user account")
    parser.add_argument('-l', '--list', dest='list_slug',
                        help='list slug with --user as list owner')
    parser.add_argument('-o', '--outdir',
                        help='output directory')
    args = parser.parse_args()
    return args
