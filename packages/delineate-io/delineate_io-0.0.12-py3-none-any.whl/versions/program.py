#!/usr/bin/env python

class Program(object):
    """ """
    
    def __init__(self, name, version):
        """ """

        self.name = str(name)

        if version[:1] is not "v":
            self.version = "v{}".format(version)
        else:
            self.version = version