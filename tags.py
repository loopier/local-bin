#!/usr/bin/python
import argparse
import os
import configparser
import glob

parser = argparse.ArgumentParser(description="Tag system for files.")
parser.add_argument('-p', '--path', metavar="", help="path to the tags directory")
# parser.add_argument('-t', '--tags', action="append", nargs='+', metavar="", help="path to the tags directory")
parser.add_argument('-f', '--filename', metavar="", help="name of the file to tag")
parser.add_argument('tags', action="append", nargs='*', metavar="", help="list of tags")
parser.add_argument('-d', '--delete', metavar="", help="remove tags")
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
    try:
        return os.stat(filename).st_ino
    except FileNotFoundError:
        return None

def getUniqueTags(tags):
    """Return unique tags in list."""
    return sorted(list(set(tags)))

def getLinksWith(searchstrings):
    """Return LINKS with SEARCHSTR."""
    print("parsing links looking for: {}".format(searchstrings))

    taggedfiles = ""

    for i, searchstring in enumerate(searchstrings):
        taggedfiles = glob.glob("{}/*{}*".format(tagspath, searchstring))

    return taggedfiles

def getLinksWithInode(inode):
    """Return files with INODE."""
    return getLinksWith([inode])

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
        tag = os.path.basename(link).split(':')[1:]
        tags = tags + tag
        # print(tag)

    tags = getUniqueTags(tags)
    print("Tags for {}: {}".format(filename, tags))
    return tags


def hasTag(filename, tag):
    """Returns TRUE if FILENAME already has the TAG."""
    return false

def fileIsTagged(filename):
    """Returns TRUE if FILENAME already has tags."""
    tagged = glob.glob("{}/*{}*".format(tagspath, getFileInode(filename)))
    return (len(tagged) > 0)


def createTagString(tags):
    """Returns a string with TAGS separated by ':'"""
    tagstr = ""
    for tag in tags:
        # if tag in existingfiletags:
        #     print("'{}' already has the tag #{} ... skipping".format(filename, tag))
        #     continue
        # else:
        #     tagstr += ":{}".format(tag)
        tagstr += ":{}".format(tag)
    return tagstr

def createTagLink(filename, tags):
    """Creates a symlink named TAGSTR in the tags directory targetting FILENAME."""
    fileId = getFileInode(filename)
    # TODO: figure out if it's better to include the filename in the symlink string
    # basename = os.path.basename(filename)
    # tagstr = "{}/{}:{}".format(tagspath, fileId, basename)
    tagstr = createTagString(tags)
    linkpath = "{}/{}{}".format(tagspath, fileId, tagstr)
    print("filename: {}".format(filename))
    print("linkpath: {}".format(linkpath))
    print("tagspath: {}".format(tagspath))
    print("id: {}".format(fileId))

    try:
        os.symlink(filename, linkpath)
    except FileExistsError:
        print("File alrady has all tags: {} ... skipping".format(tagstr))
    print("link cmd: {}".format(linkpath))

def deleteTagLink(link):
    """Deletes the LINK."""
    linkpath = "{}/*{}*".format(tagspath, link)
    for f in glob.glob(linkpath):
        os.remove(f)


def addTags(filename, newtags):
    """Tags a FILENAME with a list of TAGS."""
    print("file is tagged: {}".format(fileIsTagged(filename)))

    existingfiletags = []

    if (fileIsTagged(filename)):
        existingfiletags = getFileTags(filename)
        deleteTagLink(getFileInode(filename))

    tags = getUniqueTags(newtags + existingfiletags)
    createTagLink(filename, tags)
    print("Tags: {}".format(tags))

def removeTags(filename, tags):
    """Remove TAGS from FILENAME."""
    oldtags = getFileTags(filename)
    print("Removing {} from {}".format(tags, oldtags))


if __name__ == "__main__":
    loadConfig()

    if args.filename:
        if len(args.tags[0]) == 0:
            getFileTags(args.filename)
        else:
            if args.delete:
                print("delete")
                # TODO fix DELETE
                removeTags(args.filename, args.tags[0])
            else:
                addTags(args.filename, args.tags[0])
    else:
        listFiles(args.tags[0])


    if args.quiet:
        print("...")
    elif args.verbose:
        verbose = True
