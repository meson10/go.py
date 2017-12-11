#!/usr/bin/env python3

import os
import sys
import os.path
import subprocess
import distutils.spawn
from argparse import ArgumentParser


GO = "go"
GOPATH = "gopath"
README = "https://golang.org/doc/install"

def walkUp(bottom):
    """Mimic walk but in reverse"""
    bottom = os.path.realpath(bottom)
    dirs = []


def which(name):
    """
    Find the executable location for that name. Works cross-platform.
    """
    return distutils.spawn.find_executable(name)

def isGoInPath():
    """
    Returns bool, if go can be found installed on your system.
    """
    return True if which(GO) else False


def getCwd():
    """
    Find the cwd. Usually the location where this script was invoked.
    """
    return os.getcwd()
    # return os.path.dirname(os.path.abspath(__file__))

def findGoPath(cwd, dest=GOPATH):
    """
    Walks up the tree of your current dir and looks for a directory called
    gopath. In case you disagree with gopath being called gopath, just pass
    the second argument.
    """
    path = os.path.realpath(cwd)
    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if fname == dest and os.path.isdir(fpath):
            return fpath

    if path == "/":
        return

    return findGoPath(os.path.join(cwd, ".."))


def setGoPath(path):
    sys.stderr.write("Setting GOPATH to %s" % path)
    new_env = os.environ.copy()
    new_env["GOPATH"] = path

    for name in ["bin", "src", "pkg"]:
        dpath = os.path.join(path, name)
        if os.path.isdir(dpath):
            continue

        os.mkdir(dpath)

    new_env["PATH"] += os.pathsep + os.pathsep.join([
        os.path.join(path, "bin")
    ])

    return new_env

def missingGO(url=README):
    sys.stderr.write("Cannot find GO in $PATH. Please follow the instructions here %s" % url)


def execute(cmd, gopath):
    p = subprocess.Popen(cmd, env=setGoPath(gopath))
    p.wait()


def create_symlink(src, dest):
    dirname = src.rsplit("/", 1)[-1]
    try:
        print("Making dir %s" % dest)
        os.makedirs(dest)
    except FileExistsError:
        pass

    link = os.path.join(dest, dirname)
    try:
        print("Making Symlink %s" % link)
        os.symlink(src, link)
    except FileExistsError:
        pass

    return link


def main(args):
    if not isGoInPath():
        missingGO()
        sys.exit(1)

    gopath = findGoPath(getCwd())
    if not gopath:
        sys.stderr.write("Cannot find any GOPATH")
        sys.exit(1)

    if args.link:
        dest_dir = os.path.join(gopath, args.dest)
        create_symlink(args.link, dest_dir)
        sys.exit(1)
        return

    try:
        execute(sys.argv[1:], gopath)
    except KeyboardInterrupt as e:
        sys.stderr.write("Ctrl-C called")
        sys.exit(1)


def dir_abspath(name):
    return os.path.abspath(name)


def cli_parser():
    args = ArgumentParser(description="go.py")
    args.add_argument("--link", dest="link",
                      type=dir_abspath,
                      help="Dir to link")

    args.add_argument("--dest", dest="dest",
                      help="package/structure/")

    return args


if __name__ == "__main__":
    cli = cli_parser()
    args, _ = cli.parse_known_args()
    main(args)
