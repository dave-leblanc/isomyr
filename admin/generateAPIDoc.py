#!/usr/bin/python
import re
from inspect import getargs, getmembers, ismethod

from twisted.python.filepath import FilePath


DESTINATION = "./docs/API.txt"
TEMPLATE = """\
===================
API Quick Reference
===================

Below are listed the objects and the methods that are available in the Isomyr
library.

%s
"""

def getMethods(klass):
    output = "\n"
    for methodName, method in getmembers(klass, ismethod):
        addMethod = True
        if methodName.startswith("_"):
            addMethod = False
        if methodName.startswith("__"):
            addMethod = True
        if addMethod:
            output += " * %s" % methodName
        else:
            continue
        code = method.im_func.func_code
        args, ignored, ignored = getargs(code)
        args_no_self = ", ".join(args[1:])
        if not args_no_self:
            output += " (takes no parameters)\n\n"
            continue
        if "," in args_no_self:
            prepend = "parameters: "
        else:
            prepend = "parameter: "
        output += "\n\n   * %s%s\n\n" % (prepend, args_no_self)
    return output.strip("\n")


def fillTemplate():
    sourceLines = FilePath(SOURCE).getContent().split("\n")
    data = TEMPLATE % {
        "rest": getMethods(RESTAspect),
        "data": getMethods(StaticDataAspect),
        "atom": getMethods(AtomAspect),
        "cache": getMethods(Cache),
        }
    apiDoc = FilePath(DESTINATION)
    apiDoc.touch()
    apiDoc.setContent(data)


if __name__ == "__main__":
    fillTemplate()
