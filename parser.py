# This module is responsible for parsing the output files from floss and creating 
# representation of the dataset that can be used for training and testing.

import os
import json

class FlossParser:
    def __init__(self, directory):
        self.directory = directory
        self.data = []