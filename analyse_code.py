#!/usr/bin/python

import subprocess

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Code analyzer to produce .classes description')
    parser.add_argument('--sources','-s', help='The disrectory where the sources are loacted',required=True)

    args = parser.parse_args()
    args = vars(args)
    print args
