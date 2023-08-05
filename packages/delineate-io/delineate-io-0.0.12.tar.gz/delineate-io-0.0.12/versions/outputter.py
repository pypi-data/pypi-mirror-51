#!/usr/bin/env python

import json

class JsonOutputter(object):
    """Outputs the program info as Json to either the console or file"""

    def __init__(self, file_name = None):
        """Initializes the Json Outputter

        Args:
            file_name (str): Optional name of the file.
        """

        self.file_name = file_name

    def output(self, items):
        """Outputs the program info as Json

        Args:
            items (list): The list of program info.
        """

        jdict = {item.name: item.version for item in items}

        if self.file_name is None:
            self.output_to_console(jdict)
        else:
            self.output_to_file(jdict)

    def output_to_console(self, jdict):
        """Outputs the program info as Json to the console

        Args:
            jdict (dict): The dict of program info.
        """

        print(json.dumps(jdict, sort_keys=True, indent=4))

    def output_to_file(self, jdict):
        """Outputs the program info as Json to a file

        Args:
            jdict (dict): The dict of program info.
        """
        
        with open(self.file_name, 'w') as file:
            json.dump(jdict, file, sort_keys=True, indent=4)

    
