# Very basic Python wrapper for enfragmo

import sys, os


def main():
    os.system('./%s S.T %s' % (sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()