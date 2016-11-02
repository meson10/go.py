#!/usr/bin/env python

import os
import sys
import os.path
import subprocess
import distutils.spawn

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
    print "Setting GOPATH to %s" % path
    os.environ["GOPATH"] = path

    for name in ["bin", "src", "pkg"]:
        dpath = os.path.join(path, name)
        if os.path.isdir(dpath):
            continue

        os.mkdir(dpath)

    os.environ["PATH"] += os.pathsep + os.pathsep.join([
        os.path.join(path, "bin")
    ])


def missingGO(url=README):
    print "Cannot find GO in $PATH. Please follow the instructions here %s" % (
        url)


def execute(cmd):
    subprocess.call(cmd)


def main():
    if not isGoInPath():
        missingGO()
        sys.exit(1)

    gopath = findGoPath(getCwd())
    if not gopath:
        print "Cannot find any GOPATH"
        sys.exit(1)

    setGoPath(gopath)
    execute(sys.argv[1:])

if __name__ == "__main__":
    main()
