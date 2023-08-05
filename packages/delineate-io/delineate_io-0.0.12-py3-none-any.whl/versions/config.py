#!/usr/bin/env python

class Config(object):
    """ """

    def __init__(self, row):
        """ """
        
        self.name = row[0]
        self.command = row[1] 

        if len(row) > 2:
            self.formatter = row[2]
        else:
            self.formatter = "extract"
        
        if len(row) > 3:
            self.position = int(row[3])
        else:
            self.position = 1
