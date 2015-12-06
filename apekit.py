"""
    Top Level Pipeline Module
    EC521 Cyber Security Project
    
    Copyright 2015 Luke Sorenson
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import fnmatch
import os


class Pipeline(object):
    """
    Top level module for apekit, which reads the list of downloaded apps,
    decompiles them into java files, reads in the java files and runs the
    lines through a variety of security modules to look for common
    vulnerabilities. These vulnerabilities are then aggregated in a
    database so that we can compute statistics.
    """

    def __init__(self):
        self.counter = 0

    @staticmethod
    def analyze_file_for_vulns(path_to_file):
        with open(path_to_file) as f:
            for line in f:
                line = line.rstrip()
                # Call the vulnerability analysis modules here.
                if len(line) > 0:
                    print line
                pass

    @staticmethod
    def get_java_files_in_dir(directory):
        """
        Returns a list of all java file paths in a directory.
        """
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.java'):
                matches.append(os.path.join(root, filename))
        return matches


if __name__ == "__main__":
    pipeline = Pipeline()
    files = pipeline.get_java_files_in_dir('test/downtyme/')
    for path_to_file in files:
        pipeline.analyze_file_for_vulns(path_to_file)