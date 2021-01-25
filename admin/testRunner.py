#!/usr/bin/env python
import os
from unittest import TestSuite, TextTestRunner
from doctest import DocFileSuite

from isomyr import meta
from isomyr.testing.suite import (
    findTests, importModule, buildUnittestSuites, buildDoctestSuite)

from admin import testDocs


searchDirs = [meta.library_name]
suites = buildUnittestSuites(paths=searchDirs)
suites.extend(testDocs.suites)

if __name__ == '__main__':
    runner = TextTestRunner(verbosity=2)
    runner.run(TestSuite(suites))
