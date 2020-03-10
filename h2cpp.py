#!/usr/bin/python

# Create a .cpp implementation file from a given .h header file
# 
# WARNING!!
# -----------
# - As for now, it only handles header files with ONLY ONE CLASS declaration
# - It DOES NOT CHECK if METHODS already EXIST, so they will be doubled if
#   they're already implemented
# - RETURN will have to be ADDED MANUALLY for methods that have return type
# - Methods with DEFAULT ARGUMENTS will be redeclared... this is a BUG and 
#   I'll fix is as soon as I can.  You will need to fix this manually by now
import sys
import os
import re

# clear console
os.system('clear')

args = sys.argv

if len(args) < 2:
    print 'Provide the path to the header file to be implemented.'
    sys.exit()

fullPath = args[1]
path = None
haederFileName = None
headerFile = None
cppFileName = None
cppFile = None


# get header file name
if os.path.isfile(fullPath) == False:
    print 'The file \'' + fullPath +'\' does not exist.'
    sys.exit()

# get class name
def getClassName(lines):
    className = "No class name found"
    for line in lines:
        if re.search('^class', line):
            className = re.sub('^class','', line.split(':')[0])
            # remove leading and trailing white spaces if any
            className = className.strip()

    return className


# get list of methods
def getMethods(lines):
    methods = []
    for line in lines:
        if re.search('\);', line):
            line = line.strip() # remove leading and trailing white spaces if any
            methods.append(line)
            pass 
        pass
    return methods

# check if given item has a parenthesis
def hasParenthesis(item):
    bParenthesis = False
    index = -1
    if re.search('\(', item):
        bParenthesis = True
        index = item.index('(')
    return bParenthesis, index

def getMethodName(method):
    name = "Error on getting method name"
    items = method.split(' ')
    for item in items:
        bParenthesis, parenthesisIndex = hasParenthesis(item)
        if bParenthesis:
            if parenthesisIndex > 0:
                name = item.split('(')[0]
            elif parenthesisIndex == 0:
                name = items[items.index(item) - 1]
    return name

# add '[ClassName]::' and body to given methods
def implementMethods(methodList, classname):
    for method in methodList:
        index = methodList.index(method)
        # print 'Implementing: ' + method + ' with \'' + classname +'::\''
        methodName = getMethodName(method)
        method = method.replace(methodName, classname + '::' + methodName) # prepend class name
        method = method.replace(';', '\n{\n\t// !!! TO DO\n}\n') # add body
        methodList[index] = method
    return methodList

# separate header file name from full path
path, headerFileName = os.path.split(fullPath)
# if path is empty set it to current directory
if len(path) < 1:
    path = os.getcwd()

# open header file
headerFile = open(path+'/'+headerFileName, 'r')
headerLines = headerFile.readlines()

className = getClassName(headerLines)
# implment methods
methods = getMethods(headerLines)
implementedMethods = implementMethods(methods, className)

# check if .cpp file exists
# open it with append mode if it does, create it otherwise
cppFileName = headerFileName.replace('.h','.cpp')
cppFile = None
cppFileExisted = os.path.isfile(path+'/'+cppFileName)
cppFile = open(path+'/'+cppFileName, 'a')

# append implemented method to .cpp file
finalImplementationString = ""
if cppFileExisted == False:
    finalImplementationString = '#include \"' + headerFileName + '\"\n'
finalImplementationString = finalImplementationString + '\n' + '\n///\n'.join(implementedMethods)
# print finalImplementationString
cppFile.write(finalImplementationString)

# console output
print 'Implementing ' + headerFileName
print ''
print 'Path: ' + path
print 'File: ' + headerFileName
print 'Class name: \'' + className +'\''
if cppFileExisted:
    print '\'' + cppFileName + '\'' + ' already exists.'
    print 'Implemented methods will be appended at the end of the existing file.'
else:
    print '\'' + cppFileName + '\'' + ' file was not found.  It will be created for you.'
print str(len(methods)) + ' methods where implemented.' 
print ''
