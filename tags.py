#!/usr/bin/python
import argparse
import os
import configparser
import glob

parser = argparse.ArgumentParser(description="Tags system for files.")
parser.add_argument('-p', '--path', metavar="", help="path to the tags directory")
# parser.add_argument('-t', '--tags', action="append", nargs='+', metavar="", help="path to the tags directory")
parser.add_argument('tags', action="append", nargs='*', metavar="", help="list of tags")
parser.add_argument('-f', '--filename', help="name of the file to tag")
group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action="store_true", help="print quiet")
group.add_argument('-v', '--verbose', action="store_true", help="print verbose")
args = parser.parse_args()

defaultconfigpath = os.path.expanduser("~/.config/tagsrc")
configpath = defaultconfigpath
config = configparser.ConfigParser()

tagspath = None
verbose = False
quiet = False

def loadConfig():
    """Load configuration file."""
    config.read(configpath)
    global tagspath
    tagspath = os.path.expanduser(config["default"]["path"])

def getFileInode(filename):
    """Return the inode number for FILENAME"""
    return os.stat(filename).st_ino

def getLinksWith(searchstrings):
    """Return LINKS with SEARCHSTR."""
    print("parsing links looking for: {}".format(searchstrings))

    for i, searchstring in enumerate(searchstrings[0]):
        taggedfiles = glob.glob("{}/*{}*".format(tagspath, searchstring))

    return taggedfiles

def getLinksWithInode(inode):
    """Return files with INODE."""
    return getLinksWith(inode)

def getLinksWithTags(tags):
    """Return files with TAG."""
    return getLinksWith(tags)

def listFiles(tags):
    """List files with TAG."""
    links = getLinksWithTags(tags)

    for link in links:
        print(os.readlink(link))

def getFileTags(filename):
    """Return FILENAME tags."""
    inode = getFileInode(filename)
    links = getLinksWithTags(str(inode))
    # print("file: {}".format(filename))
    # print("inode: {}".format(inode))
    # print("links: {}".format(links))

    tags = []
    for link in links:
        tags = tags + os.path.basename(link).split(':')[1:]

    # get unique values
    tags = (list(set(tags)))
    print("Tags for {}: {}".format(filename, tags))
    return tags

def tagFile(filename, tags):
    """Tags a FILENAME with a list of TAGS."""
    fileId = getFileInode(filename)
    basename = os.path.basename(filename)
    # TODO: figure out if it's better to include the filename in the symlink string
    # tagstr = "{}/{}:{}".format(tagspath, fileId, basename)
    tagstr = "{}/{}".format(tagspath, fileId)

    for tag in tags[0]:
        tagstr += ":{}".format(tag)

    os.symlink(filename, tagstr)
    # print("link cmd: {}".format(tagstr))

    if verbose:
        print("{} tags where added to '{}' - {}".format(tags, filename, tagstr))
    elif quiet:
        pass
    else:
        print("'{}' tagged with {}".format(filename, tags))

if __name__ == "__main__":
    loadConfig()

    if args.filename:
        if len(args.tags[0]) == 0:
            getFileTags(args.filename)
        else:
            tagFile(args.filename, args.tags)
    else:
        listFiles(args.tags)

    if args.quiet:
        print("...")
    elif args.verbose:
        verbose = True
